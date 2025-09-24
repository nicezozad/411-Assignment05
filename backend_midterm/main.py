# main.py  (no logging, no backup)
from __future__ import annotations
import sqlite3, random
from datetime import datetime, date, time as dtime, timedelta
from typing import List, Tuple, Iterable

from fastapi import FastAPI, HTTPException, Request
from sqlmodel import Session, select
from sqlalchemy import update, and_

from database import engine, init_db
from model import (
    Line, Station, Service, ServiceStop, ServiceCar, Ticket,
    ServiceCreate, ServiceBasicOut, ServiceDetailOut, ServiceStopOut, StationOut,
    ServiceCarOut, TicketRequest, TicketOut,
    DirectionEnum, CarTypeEnum,
)

# ---------- DB init ----------
init_db()
app = FastAPI(title="Railway API – time-aware booking (no log / no backup)")

# ---------- Helpers ----------
DEFAULT_CARS: List[Tuple[str,int,int]] = [
    (CarTypeEnum.First.value,        1, 40),
    (CarTypeEnum.Reserved.value,     2, 64),
    (CarTypeEnum.NonReserved.value,  2, 72),
    (CarTypeEnum.Quiet.value,        1, 36),
    (CarTypeEnum.Catering.value,     1, 0),
]

def _get_or_create_line(session: Session, th: str, en: str) -> Line:
    line = session.exec(select(Line).where(Line.name_en == en)).first()
    if not line:
        line = Line(name_th=th, name_en=en)
        session.add(line); session.commit(); session.refresh(line)
    return line

def _get_or_create_station(session: Session, th: str, en: str) -> Station:
    st = session.exec(select(Station).where(Station.name_en == en)).first()
    if not st:
        st = Station(name_th=th, name_en=en)
        session.add(st); session.commit(); session.refresh(st)
    return st

def _ensure_stations(session: Session, pairs: Iterable[Tuple[str,str]]) -> List[int]:
    return [_get_or_create_station(session, th, en).id for th, en in pairs]

def _guess_dep_arr(code: str, base_day: date | None = None) -> tuple[datetime, datetime]:
    """สุ่ม/กำหนดเวลาออก-ถึงแบบ deterministic จากรหัสขบวน เพื่อให้ค้นตามเวลาได้จริง"""
    if base_day is None:
        base_day = date.today()
    # กระจายช่วง 05:30–23:00
    rnd = (abs(hash(code)) % (17*60)) + (5*60 + 30)
    dep = datetime.combine(base_day, dtime(hour=rnd//60, minute=rnd%60))
    uc = code.upper()
    hours = 5
    if "SPECIAL" in uc or "EXPRESS" in uc: hours = 3
    elif "RAPID" in uc: hours = 4
    elif "LOCAL" in uc or "COMMUTER" in uc or "ORDINARY" in uc: hours = 5 + (abs(hash(code)) % 2)
    arr = dep + timedelta(hours=hours, minutes=random.randint(0,50))
    return dep, arr

def _create_service_with_stops_and_cars(
    session: Session, line_id: int, code: str, origin_en: str, direction: str,
    stop_ids_in_order: List[int], departure_time: datetime | None = None, arrival_time: datetime | None = None,
    cars: Iterable[Tuple[str,int,int]] = DEFAULT_CARS
) -> Service:
    dep, arr = (departure_time, arrival_time) if departure_time and arrival_time else _guess_dep_arr(code)
    svc = Service(
        line_id=line_id, code=code, origin=origin_en,
        direction=DirectionEnum(direction), departure_time=dep, arrival_time=arr
    )
    session.add(svc); session.commit(); session.refresh(svc)
    for i, st_id in enumerate(stop_ids_in_order, start=1):
        session.add(ServiceStop(service_id=svc.id, station_id=st_id, stop_order=i))
    for car_type, car_count, seats in cars:
        session.add(ServiceCar(service_id=svc.id, car_type=CarTypeEnum(car_type),
                               car_count=car_count, seats_per_car=seats))
    session.commit()
    return svc

# ---------- SEED DATA (ทุกสาย/สถานีตามที่ให้) ----------
# Northern
NORTHERN_STATIONS = [
    ("กรุงเทพ (หัวลำโพง)","BANGKOK"),("สามเสน","Sam Sen"),("ชุมทางบางซื่อ","BANG SUE JUNCTION"),
    ("กรุงเทพอภิวัฒน์","KRUNG THEP APHIWAT CENTRAL TERMINAL"),("ดอนเมือง","DON MUANG"),("รังสิต","RANGSIT"),
    ("เชียงราก","Chiang Rak"),("บางปะอิน","Bang Pa-in"),("อยุธยา","AYUTTHAYA"),
    ("ชุมทางบ้านภาชี","BAN PHACHI JUNCTION"),("หนองวิวัฒน์","Nong Wiwat"),("ท่าเรือ","Tha Ruea"),
    ("บ้านหมอ","Ban Mo"),("หนองโดน","Nong Don"),("บ้านกลับ","Ban Klap"),("บ้านป่าหวาย","Ban Pa Wai"),
    ("ลพบุรี","LOP BURI"),("โคกกะเทียม","Khok Kathiam"),("บ้านหมี่","Ban Mi"),("จันเสน","Chan Sen"),
    ("ช่องแค","Chong Khae"),("บ้านตาคลี","Ban Takhli"),("หัวหวาย","Hua Wai"),("หนองโพ","Nong Pho"),
    ("เนินมะกอก","Noen Makok"),("เขาทอง","Khao Thong"),("นครสวรรค์","NAKHON SAWAN"),("ปากน้ำโพ","Pak Nam Pho"),
    ("ทับกฤช","Thap Krit"),("ชุมแสง","Chum Saeng"),("บางมูลนาก","Bang Mun Nak"),("ตะพานหิน","TAPHAN HIN"),
    ("วังกรด","Wang Krot"),("พิจิตร","PHICHIT"),("ท่าฬ่อ","Tha Lo"),("บางกระทุ่ม","Bang Krathum"),
    ("บ้านใหม่","Ban Mai"),("พิษณุโลก","PHITSANULOK"),("พรหมพิราม","Phrom Phiram"),("หนองตม","Nong Tom"),
    ("พิชัย","Phichai"),("ชุมทางบ้านดารา","Ban Dara Junction"),("สวรรคโลก","Sawankhalok"),
    ("ท่าสัก","Tha Sak"),("ตรอน","Tron"),("อุตรดิตถ์","UTTARADIT"),("ศิลาอาสน์","Sila At"),
    ("เด่นชัย","DEN CHAI"),("บ้านปิน","Ban Pin"),("แม่เมาะ","Mae Mo"),("นครลำปาง","NAKHON LAMPANG"),
    ("ขุนตาน","Khun Tan"),("ลำพูน","Lamphun"),("เชียงใหม่","CHIANG MAI"),
]
NORTHERN_FROM_BKK = ["COMMUTER 303","LOCAL 401","ORDINARY 201","ORDINARY 209","ORDINARY 211","ORDINARY 207","ORDINARY 301","COMMUTER 317","COMMUTER 313"]
NORTHERN_FROM_KTA = ["RAPID 111","SPECIAL EXPRESS (DIESEL RAILCAR) 7**","RAPID 109","SPECIAL EXPRESS (UTTARAWITHI) 9","SPECIAL EXPRESS 13","RAPID 107","EXPRESS 51"]
NORTHERN_TO_BKK   = ["COMMUTER 302","LOCAL 410","ORDINARY 208","COMMUTER 304","ORDINARY 212","ORDINARY 202","LOCAL 402","LOCAL 408"]
NORTHERN_TO_KTA   = ["RAPID 108","EXPRESS 52","SPECIAL EXPRESS 14","SPECIAL EXPRESS (UTTARAWITHI) 10","RAPID 112","SPECIAL EXPRESS (DIESEL RAILCAR) 8**","RAPID 102"]

# Northeastern (อีสาน)
NORTHEAST_STATIONS = [
    ("กรุงเทพ (หัวลำโพง)","BANGKOK"),("สามเสน","Sam Sen"),("ชุมทางบางซื่อ","BANG SUE JUNCTION"),
    ("กรุงเทพอภิวัฒน์","KRUNG THEP APHIWAT CENTRAL TERMINAL"),("ดอนเมือง","DON MUANG"),("รังสิต","RANGSIT"),
    ("อยุธยา","AYUTTHAYA"),("ชุมทางบ้านภาชี","BAN PHACHI JUNCTION"),("สระบุรี","SARABURI"),
    ("ชุมทางแก่งคอย","Kaeng Khoi Junction"),("มวกเหล็ก","Muak Lek"),("ปากช่อง","Pak Chong"),
    ("สีคิ้ว","Sikhio"),("สูงเนิน","Sung Noen"),("กุดจิก","Kut Chik"),("โคกกรวด","Khok Kruat"),
    ("นครราชสีมา","NAKHON RATCHASIMA"),("ชุมทางถนนจิระ","Thanon Chira Junction"),
    ("แก่งเสือเต้น","Kaeng Suea Ten"),("เขื่อนป่าสักชลสิทธิ์","Pa Sak Jolasid Dam"),("ลำนารายณ์","Lam Narai"),
    ("บำเหน็จณรงค์","Bamnet Narong"),("จัตุรัส","Chatturat"),("บ้านเหลื่อม","Ban Luam"),
    ("เมืองคง","Mueang Khong"),("ชุมทางบัวใหญ่","Bua Yai Junction"),("เมืองพล","Mueang Phon"),
    ("บ้านไผ่","Ban Phai"),("ขอนแก่น","KHON KAEN"),("น้ำพอง","Nam Phong"),
    ("กุมภวาปี","Kumphawapi"),("อุดรธานี","UDON THANI"),("หนองคาย","NONG KHAI"),("ท่านาแล้ง","THANALENG"),
    ("จักราช","Chakkarat"),("ห้วยแถลง","Huai Thalaeng"),("ลำปลายมาศ","Lam Plai Mat"),("บุรีรัมย์","Buri Ram"),
    ("กระสัง","Krasang"),("ลำชี","Lam Chi"),("สุรินทร์","SURIN"),("ศีขรภูมิ","Sikhoraphum"),
    ("สำโรงทาบ","Samrong Thap"),("อุทุมพรพิสัย","Uthumphon Phisai"),("ศรีสะเกษ","SI SA KET"),
    ("กันทรารมย์","Kanthararom"),("อุบลราชธานี","UBON RATCHATHANI"),
]
NE_FROM_BKK = ["COMMUTER 339","ORDINARY 233","COMMUTER 341","LOCAL 421","LOCAL 415","LOCAL 419","LOCAL 427","LOCAL 431","LOCAL 433","LOCAL 435","LOCAL 437","LOCAL 417","LOCAL 429"]
NE_FROM_KTA = ["SPECIAL EXPRESS (DIESEL RAILCAR) 21**","EXPRESS (DIESEL RAILCAR) 75*","EXPRESS (DIESEL RAILCAR) 71**","RAPID 139","SPECIAL EXPRESS 25","RAPID 141"]
NE_TO_BKK   = ["COMMUTER 342","LOCAL 424","ORDINARY 234","LOCAL 420","LOCAL 422","LOCAL 426","LOCAL 428","LOCAL 416","LOCAL 432","MIXED 482","MIXED 484"]
NE_TO_KTA   = ["RAPID 142","EXPRESS 24","RAPID 140","SPECIAL EXPRESS 72*","RAPID 136","SPECIAL EXPRESS 22*","RAPID 134","SPECIAL EXPRESS 26","RAPID 132"]

# Eastern
EASTERN_STATIONS = [
    ("กรุงเทพ (หัวลำโพง)","Bangkok"),("ยมราช","Yommarat"),("อุรุพงษ์","Urupong"),("พญาไท","Phaya Thai"),
    ("มักกะสัน","Makkasan"),("อโศก","Asok"),("คลองตัน","Khlong Tan"),("สุขุมวิท 71","Sukhumvit 71"),
    ("หัวหมาก","Hua Mak"),("บ้านทับช้าง","Ban Thap Chang"),("ซอยวัดลานบุญ","Soi Wat Lan Bun"),
    ("ลาดกระบัง","Lat Krabang"),("พระจอมเกล้า","Phra Chom Klao"),("หัวตะเข้","Hua Takhe"),
    ("คลองหลวงแพ่ง","Khlong Luang Phaeng"),("คลองอุดมชลจร","Khlong Udom Chonlachon"),("เปรง","Preng"),
    ("คลองแขวงกลั่น","Khlong Khwaeng Klan"),("คลองบางพระ","Khlong Bang Phra"),("บางเตย","Bang Toei"),
    ("ชุมทางฉะเชิงเทรา","Chachoengsao Junction"),("บางน้ำเปรี้ยว","Bang Nam Priao"),
    ("ชุมทางคลองสิบเก้า","Khlong Sip Kao Junction"),("โยทะกา","Yothaka"),("บ้านสร้าง","Ban Sang"),
    ("บ้านปากพลี","Ban Pak Phli"),("ปราจีนบุรี","Prachinburi"),("โคกมะกอก","Khok Makok"),
    ("ประจันตคาม","Prachantakham"),("บ้านดงบัง","Ban Dong Bang"),("บ้านพรหมแสง","Ban Phrom Saeng"),
    ("กบินทร์บุรี","Kabin Buri"),("หนองสัง","Nong Sang"),("พระปรง","Phra Prong"),("ศาลาลำดวน","Sala Lamduan"),
    ("สระแก้ว","Sa Kaeo"),("ท่าเกษม","Tha Kasem"),("ห้วยโจด","Huai Chot"),("วัฒนานคร","Watthana Nakhon"),
    ("ห้วยเดื่อ","Huai Duea"),("อรัญประเทศ","Aranyaprathet"),("ด่านพรมแดนบ้านคลองลึก","Ban Khlong Luk Border"),
    ("แปดริ้ว","Paet Rio"),("ดอนสีนนท์","Don Si Non"),("พานทอง","Phan Thong"),("ชลบุรี","Chon Buri"),
    ("บางพระ","Bang Phra"),("เขาพระบาท","Khao Phra Bat"),("ชุมทางศรีราชา","Si Racha Junction"),
    ("บางละมุง","Bang Lamung"),("พัทยา","Pattaya"),("พัทยาใต้","Pattaya Tai"),("ตลาดน้ำ 4 ภาค","Talat Nam 4 Pak"),
    ("บ้านห้วยขวาง","Ban Huai Khwang"),("ญาณสังวราราม","Yanasangwararam"),("สวนนงนุช","Suan Nongnut"),
    ("ชุมทางเขาชีจรรย์","Khao Chi Chan Junction"),("บ้านพลูตาหลวง","Ban Phlu Ta Luang"),
]
EAST_FROM_BKK = ["ORDINARY 275","DIESEL 997","ORDINARY 283","DIESEL 281","COMMUTER 367","COMMUTER 389","DIESEL 279","DIESEL 277","COMMUTER 379","COMMUTER 391","COMMUTER 371","COMMUTER 383"]
EAST_TO_BKK   = ["ORDINARY 276","DIESEL 998","ORDINARY 284","DIESEL 282","COMMUTER 368","COMMUTER 390","DIESEL 280","DIESEL 278","COMMUTER 380","COMMUTER 392","COMMUTER 372","COMMUTER 384"]

# Wongwian Yai – Maha Chai
WYM_STATIONS = [
    ("วงเวียนใหญ่","Wongwian Yai"),("ตลาดพลู","Talat Phlu"),("วุฒากาศ","Wutthakat"),("คลองต้นไทร","Khlong Ton Sai"),
    ("จอมทอง","Chom Thong"),("วัดไทร","Wat Sai"),("วัดสิงห์","Wat Sing"),("บางบอน","Bang Bon"),
    ("การเคหะ","Kan Kheha"),("รางโพธิ์","Rang Pho"),("สามแยก","Sam Yaek"),("พรหมแดน","Phrom Daen"),
    ("ทุ่งสีทอง","Thung Si Thong"),("บางน้ำจืด","Bang Nam Chuet"),("คอกควาย","Khok Khwai"),
    ("บ้านขอม","Ban Khom"),("คลองจาก","Khlong Chak"),("นิคมรถไฟมหาชัย","Nikhom Rotfai Maha Chai"),
    ("มหาชัย","Maha Chai"),
]
WYM_OUT = ["4303","4311","4321","4341","4305","4313","4323","4343","4315","4325","4317","4307","4327","4345","4309","4329","4347"]
WYM_IN  = ["4302","4312","4322","4342","4304","4314","4324","4344","4316","4326","4318","4308","4328","4346","4310","4330","4348"]

# Ban Laem – Mae Klong
BL_STATIONS = [
    ("บ้านแหลม","Ban Laem"),("ท่าฉลอม","Tha Chalom"),("บ้านชีผ้าขาว","Ban Chi Pha Khao"),
    ("บางสีคต","Bang Si Khot"),("บางกระเจ้า","Bang Krachao"),("บ้านบ่อ","Ban Bo"),
    ("บางโทรัด","Bang Thorat"),("บ้านกาหลง","Ban Kalong"),("บ้านนาขวาง","Ban Na Khwang"),
    ("บ้านนาโคก","Ban Na Khok"),("เขตเมือง","Khet Mueang"),("ลาดใหญ่","Lat Yai"),("แม่กลอง","Mae Klong"),
]
BL_OUT = ["4381","4383","4385","4387"]
BL_IN  = ["4380","4382","4384","4386"]

# Commuter
COMMUTER_STATIONS = [
    ("กรุงเทพ (หัวลำโพง)","BANGKOK"),("สามเสน","Sam Sen"),("ชุมทางบางซื่อ","BANG SUE JUNCTION"),
    ("กรุงเทพอภิวัฒน์","KRUNG THEP APHIWAT CENTRAL TERMINAL"),
    ("ดอนเมือง","DON MUANG"),("รังสิต","RANGSIT"),("เชียงราก","Chiang Rak"),("บางปะอิน","Bang Pa-in"),
    ("อยุธยา","AYUTTHAYA"),("ชุมทางบ้านภาชี","BAN PHACHI JUNCTION"),
]
COMMUTER_OUT = ["COMMUTER 303","COMMUTER 339*","ORDINARY 201","ORDINARY 209","ORDINARY 233","ORDINARY 207","ORDINARY 301","COMMUTER 341","COMMUTER 317*","COMMUTER 313*"]
COMMUTER_IN  = ["COMMUTER 304","COMMUTER 342*","ORDINARY 202","ORDINARY 212","ORDINARY 234","ORDINARY 208","ORDINARY 302","COMMUTER 340","COMMUTER 318","COMMUTER 314"]

# Southern
SOUTHERN_STATIONS = [
    ("กรุงเทพ (หัวลำโพง)","BANGKOK"),("สามเสน","Sam Sen"),("ชุมทางบางซื่อ","BANG SUE JUNCTION"),
    ("KRUNG THEP APHIWAT CENTRAL TERMINAL","KRUNG THEP APHIWAT CENTRAL TERMINAL"),
    ("บางบำหรุ","Bang Bamru"),("ธนบุรี","THON BURI"),("ชุมทางตลิ่งชัน","Taling Chan Junction"),
    ("ศาลายา","Sala Ya"),("นครปฐม","Nakhon Pathom"),("ชุมทางหนองปลาดุก","Nong Pla Duk Junction"),
    ("สุพรรณบุรี","Suphan Buri"),("กาญจนบุรี","Kanchanaburi"),("สะพานแควใหญ่","Khwae Yai Bridge"),
    ("ท่ากิเลน","Tha Kilen"),("สะพานถ้ำกระแซ","Tham Krasae Bridge"),("วังโพ","Wang Pho"),
    ("เกาะมหามงคล","Ko Maha Mongkhon"),("น้ำตก","Nam Tok"),
    ("บ้านโป่ง","Ban Pong"),("โพธาราม","Photharam"),("ราชบุรี","Ratchaburi"),("ปากท่อ","Pak Tho"),
    ("เพชรบุรี","Phetchaburi"),("บ้านชะอำ","Ban Cha-am"),("หัวหิน","Hua Hin"),("วังก์พง","Wang Phong"),
    ("ปราณบุรี","Pran Buri"),("ประจวบคีรีขันธ์","Prachuap Khiri Khan"),("ห้วยยาง","Huai Yang"),
    ("ทับสะแก","Thap Sakae"),("บ้านกรูด","Ban Krut"),("บางสะพานใหญ่","Bang Saphan Yai"),
    ("บางสะพานน้อย","Bang Saphan Noi"),("มาบอำมฤต","Map Ammarit"),("ปะทิว","Pathio"),
    ("ชุมพร","Chumphon"),("สวี","Sawi"),("หลังสวน","Lang Suan"),("ละแม","Lamae"),
    ("ท่าชนะ","Tha Chana"),("ไชยา","Chaiya"),("สุราษฎร์ธานี","Surat Thani"),("คีรีรัฐนิคม","Khiri Ratthanikhom"),
    ("นาสาร","Na San"),("บ้านส้อง","Ban Song"),("ฉวาง","Chawang"),("คลองจันดี","Khlong Chan Di"),
    ("นาบอน","Na Bon"),("ชุมทางทุ่งสง","Thung Song Junction"),("ตรัง","Trang"),("กันตัง","Kantang"),
    ("ชุมทางเขาชุมทอง","Khao Chum Thong Junction"),("นครศรีธรรมราช","Nakhon Si Thammarat"),
    ("ชะอวด","Cha-uat"),("พัทลุง","Phatthalung"),("ชุมทางหาดใหญ่","Hat Yai Junction"),
    ("จะนะ","Chana"),("ปัตตานี","Pattani"),("ยะลา","Yala"),("ตันหยงมัส","Tanyong Mat"),
    ("สุไหงโก-ลก","SU-NGAI KOLOK"),("คลองแงะ","Khlong Ngae"),("ปาดังเบซาร์","Padang Besar"),
]
SOUTH_OUT = ["ORDINARY 261","COMMUTER 355","RAPID 171","RAPID 169","RAPID 83","EXPRESS 85","SPECIAL EXPRESS 39**","LOCAL 485","LOCAL 351"]
SOUTH_IN_PADANG = ["RAPID 168","EXPRESS 86","RAPID 170","EXPRESS 84"]
SOUTH_IN_KOLOK  = ["RAPID 172","SPECIAL EXPRESS 44**","LOCAL 486","LOCAL 352"]

# ---------- Insert per line ----------
def insert_northern(session: Session):
    line = _get_or_create_line(session,"สายเหนือ","Northern Line")
    ids_out = _ensure_stations(session,NORTHERN_STATIONS); ids_in = list(reversed(ids_out))
    for c in NORTHERN_FROM_BKK: _create_service_with_stops_and_cars(session,line.id,c,"BANGKOK","outbound",ids_out)
    for c in NORTHERN_FROM_KTA: _create_service_with_stops_and_cars(session,line.id,c,"KRUNG THEP APHIWAT CENTRAL TERMINAL","outbound",ids_out)
    for c in NORTHERN_TO_BKK:   _create_service_with_stops_and_cars(session,line.id,c,"CHIANG MAI","inbound",ids_in)
    for c in NORTHERN_TO_KTA:   _create_service_with_stops_and_cars(session,line.id,c,"CHIANG MAI","inbound",ids_in)

def insert_northeastern(session: Session):
    line = _get_or_create_line(session,"สายตะวันออกเฉียงเหนือ","Northeastern Line")
    ids_out = _ensure_stations(session,NORTHEAST_STATIONS); ids_in = list(reversed(ids_out))
    for c in NE_FROM_BKK: _create_service_with_stops_and_cars(session,line.id,c,"BANGKOK","outbound",ids_out)
    for c in NE_FROM_KTA: _create_service_with_stops_and_cars(session,line.id,c,"KRUNG THEP APHIWAT CENTRAL TERMINAL","outbound",ids_out)
    for c in NE_TO_BKK:   _create_service_with_stops_and_cars(session,line.id,c,"UBON RATCHATHANI","inbound",ids_in)
    for c in NE_TO_KTA:   _create_service_with_stops_and_cars(session,line.id,c,"NONG KHAI","inbound",ids_in)

def insert_eastern(session: Session):
    line = _get_or_create_line(session,"สายตะวันออก","Eastern Line")
    ids_out = _ensure_stations(session,EASTERN_STATIONS); ids_in = list(reversed(ids_out))
    for c in EAST_FROM_BKK: _create_service_with_stops_and_cars(session,line.id,c,"Bangkok","outbound",ids_out)
    for c in EAST_TO_BKK:   _create_service_with_stops_and_cars(session,line.id,c,"Ban Phlu Ta Luang","inbound",ids_in)

def insert_wym(session: Session):
    line = _get_or_create_line(session,"วงเวียนใหญ่–มหาชัย","Wongwian Yai–Maha Chai Line")
    ids_out = _ensure_stations(session,WYM_STATIONS); ids_in = list(reversed(ids_out))
    for c in WYM_OUT: _create_service_with_stops_and_cars(session,line.id,f"LOCAL {c}","Wongwian Yai","outbound",ids_out)
    for c in WYM_IN:  _create_service_with_stops_and_cars(session,line.id,f"LOCAL {c}","Maha Chai","inbound",ids_in)

def insert_bl(session: Session):
    line = _get_or_create_line(session,"บ้านแหลม–แม่กลอง","Ban Laem–Mae Klong Line")
    ids_out = _ensure_stations(session,BL_STATIONS); ids_in = list(reversed(ids_out))
    for c in BL_OUT: _create_service_with_stops_and_cars(session,line.id,f"LOCAL {c}","Ban Laem","outbound",ids_out)
    for c in BL_IN:  _create_service_with_stops_and_cars(session,line.id,f"LOCAL {c}","Mae Klong","inbound",ids_in)

def insert_commuter(session: Session):
    line = _get_or_create_line(session,"สายชานเมือง","Commuter Line")
    ids_out = _ensure_stations(session,COMMUTER_STATIONS); ids_in = list(reversed(ids_out))
    for c in COMMUTER_OUT: _create_service_with_stops_and_cars(session,line.id,c,"BANGKOK","outbound",ids_out)
    for c in COMMUTER_IN:  _create_service_with_stops_and_cars(session,line.id,c,"BAN PHACHI JUNCTION","inbound",ids_in)

def insert_southern(session: Session):
    line = _get_or_create_line(session,"สายใต้","Southern Line")
    ids_out = _ensure_stations(session,SOUTHERN_STATIONS); ids_in = list(reversed(ids_out))
    for c in SOUTH_OUT: _create_service_with_stops_and_cars(session,line.id,c,"BANGKOK","outbound",ids_out)
    for c in SOUTH_IN_PADANG: _create_service_with_stops_and_cars(session,line.id,c,"Padang Besar","inbound",ids_in)
    for c in SOUTH_IN_KOLOK:  _create_service_with_stops_and_cars(session,line.id,c,"SU-NGAI KOLOK","inbound",ids_in)

def insert_all_lines():
    with Session(engine) as session:
        if session.exec(select(Service)).first(): return
        insert_northern(session); insert_northeastern(session); insert_eastern(session)
        insert_wym(session); insert_bl(session); insert_commuter(session); insert_southern(session)

# ---------- (optional) ensure columns for old DB ----------
def _ensure_columns():
    try:
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(service);")
            cols = [r[1] for r in cur.fetchall()]
            if "departure_time" not in cols: cur.execute("ALTER TABLE service ADD COLUMN departure_time TEXT;")
            if "arrival_time" not in cols: cur.execute("ALTER TABLE service ADD COLUMN arrival_time TEXT;")
            conn.commit()
    except Exception:
        # เงียบไว้ตามที่ต้องการ (no log)
        pass

@app.on_event("startup")
def on_startup():
    _ensure_columns()
    insert_all_lines()

# ---------- Mappers ----------
def _svc_to_basic(s: Service) -> ServiceBasicOut:
    return ServiceBasicOut(
        id=s.id, line_id=s.line_id, code=s.code, origin=s.origin,
        direction=s.direction, departure_time=s.departure_time, arrival_time=s.arrival_time
    )

def _svc_to_detail(session: Session, s: Service) -> ServiceDetailOut:
    stops = session.exec(select(ServiceStop).where(ServiceStop.service_id == s.id).order_by(ServiceStop.stop_order)).all()
    out_stops = []
    for stp in stops:
        st = session.get(Station, stp.station_id)
        out_stops.append(ServiceStopOut(order=stp.stop_order, station=StationOut(id=st.id, name_th=st.name_th, name_en=st.name_en)))
    cars = session.exec(select(ServiceCar).where(ServiceCar.service_id == s.id)).all()
    out_cars = [ServiceCarOut(
        car_type=c.car_type, car_count=c.car_count, seats_per_car=c.seats_per_car,
        total_seats=c.total_seats, reserved_seats=c.reserved_seats, available_seats=c.available_seats
    ) for c in cars]
    return ServiceDetailOut(
        id=s.id, line_id=s.line_id, code=s.code, origin=s.origin, direction=s.direction,
        departure_time=s.departure_time, arrival_time=s.arrival_time, stops=out_stops, cars=out_cars
    )

# ---------- Endpoints ----------
@app.get("/lines")
def list_lines():
    with Session(engine) as session:
        lines = session.exec(select(Line)).all()
        return [{"id":l.id, "name_th":l.name_th, "name_en":l.name_en} for l in lines]

@app.get("/stations", response_model=List[StationOut])
def list_stations():
    with Session(engine) as session:
        sts = session.exec(select(Station).order_by(Station.name_en)).all()
        return [StationOut(id=s.id, name_th=s.name_th, name_en=s.name_en) for s in sts]

@app.get("/services", response_model=List[ServiceBasicOut])
def list_services():
    with Session(engine) as session:
        svcs = session.exec(select(Service).order_by(Service.departure_time)).all()
        return [_svc_to_basic(s) for s in svcs]

@app.get("/services/{service_id}", response_model=ServiceDetailOut)
def get_service(service_id: int):
    with Session(engine) as session:
        s = session.get(Service, service_id)
        if not s: raise HTTPException(status_code=404, detail="Service not found")
        return _svc_to_detail(session, s)

@app.post("/services", response_model=ServiceBasicOut)
def create_service(req: ServiceCreate):
    with Session(engine) as session:
        line = session.get(Line, req.line_id)
        if not line: raise HTTPException(status_code=404, detail="Line not found")
        if len(req.stop_station_ids) < 2: raise HTTPException(status_code=400, detail="Require >=2 stops")
        for sid in req.stop_station_ids:
            if not session.get(Station, sid): raise HTTPException(status_code=404, detail=f"Station {sid} not found")
        svc = _create_service_with_stops_and_cars(
            session, req.line_id, req.code, req.origin, req.direction, req.stop_station_ids,
            departure_time=req.departure_time, arrival_time=req.arrival_time
        )
        return _svc_to_basic(svc)

@app.get("/services/search", response_model=List[ServiceBasicOut])
def search_services(start: datetime, end: datetime):
    if end <= start: raise HTTPException(status_code=400, detail="end ต้องมากกว่า start")
    with Session(engine) as session:
        q = select(Service).where(Service.departure_time >= start, Service.departure_time <= end).order_by(Service.departure_time)
        svcs = session.exec(q).all()
        return [_svc_to_basic(s) for s in svcs]

@app.post("/tickets", response_model=TicketOut)
def book_ticket(req: TicketRequest, request: Request):
    with Session(engine) as session:
        svc = session.get(Service, req.service_id)
        if not svc: raise HTTPException(status_code=404, detail="Service not found")
        car = session.exec(select(ServiceCar).where(ServiceCar.service_id==req.service_id, ServiceCar.car_type==req.car_type)).first()
        if not car: raise HTTPException(status_code=404, detail="Car type not found for this service")

        # optimistic locking กัน overbooking
        retries = 3
        for _ in range(retries):
            stmt = (
                update(ServiceCar)
                .where(and_(
                    ServiceCar.id == car.id,
                    ServiceCar.version == car.version,
                    (ServiceCar.reserved_seats + req.quantity) <= (ServiceCar.car_count * ServiceCar.seats_per_car),
                ))
                .values(reserved_seats=ServiceCar.reserved_seats + req.quantity, version=ServiceCar.version + 1)
            )
            result = session.exec(stmt)
            if result.rowcount and result.rowcount > 0:
                t = Ticket(service_id=req.service_id, car_type=req.car_type, quantity=req.quantity)
                session.add(t); session.commit(); session.refresh(t)
                return TicketOut(id=t.id, service_id=t.service_id, car_type=t.car_type, quantity=t.quantity)
            session.rollback()
            car = session.exec(select(ServiceCar).where(ServiceCar.id==car.id)).one_or_none()
        raise HTTPException(status_code=409, detail="Not enough seats or concurrency conflict")

@app.get("/tickets", response_model=List[TicketOut])
def list_tickets():
    with Session(engine) as session:
        ts = session.exec(select(Ticket)).all()
        return [TicketOut(id=t.id, service_id=t.service_id, car_type=t.car_type, quantity=t.quantity) for t in ts]
