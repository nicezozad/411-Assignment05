// @ts-nocheck
/**
 * @typedef {'pass'|'warn'|'none'} SurveyStatus
 * 
 * @typedef {Object} StatusAspect
 * @property {string} slug           
 * @property {string} title          
 * @property {string=} lastUpdated   
 * @property {SurveyStatus} status   
 * @property {string=} note        
 * @property {string=} ctaLabel     
 * @property {string=} image        
 * @property {string=} imageAlt      
 */

/** @type {StatusAspect[]} */
export const aspects = [
  {
    slug: 'water',
    title: 'การจัดการน้ำ',
    lastUpdated: '26/02/2568 เวลา 19:00 น.',
    status: 'warn',
    note: 'น้ำทิ้งยังมีโอกาสปนเปื้อน',
    ctaLabel: 'แก้ไขข้อมูล',
    image: '/images/water.jpg',
    imageAlt: 'water management'
  },
  {
    slug: 'soil',
    title: 'การจัดการที่ดิน',
    lastUpdated: '26/02/2568 เวลา 19:00 น.',
    status: 'pass',
    note: 'แปลงเพาะปลูกเป็นตามมาตรฐาน',
    ctaLabel: 'ดูรายละเอียด',
    image: '/images/soil.jpg',
    imageAlt: 'soil management'
  },
  {
    slug: 'fert-chem',
    title: 'การใช้ปุ๋ยและยา',
    status: 'none',
    note: 'ไม่มีการบันทึกข้อมูล',
    ctaLabel: 'เพิ่มข้อมูล',
    image: '/images/fertilizer.jpg',
    imageAlt: 'fertilizer and chemical usage'
  },
  {
    slug: 'tools',
    title: 'ยานพาหนะ อุปกรณ์',
    status: 'none',
    note: 'ไม่มีการบันทึกข้อมูล',
    ctaLabel: 'เพิ่มข้อมูล',
    image: '/images/tools.jpg',
    imageAlt: 'tools and equipment'
  },
  {
    slug: 'harvest',
    title: 'การเก็บเกี่ยว',
    status: 'none',
    note: 'ไม่มีการบันทึกข้อมูล',
    ctaLabel: 'เพิ่มข้อมูล',
    image: '/images/harvest.jpg',
    imageAlt: 'harvest process'
  },
  {
    slug: 'postharvest',
    title: 'การพักผลผลิต',
    status: 'none',
    note: 'ไม่มีการบันทึกข้อมูล',
    ctaLabel: 'เพิ่มข้อมูล',
    image: '/images/postharvest.jpg',
    imageAlt: 'postharvest storage'
  },
  {
    slug: 'facilities',
    title: 'สถานที่ต่าง ๆ',
    status: 'none',
    note: 'ไม่มีการบันทึกข้อมูล',
    ctaLabel: 'เพิ่มข้อมูล',
    image: '/images/facilities.jpg',
    imageAlt: 'facilities and environment'
  },
  {
    slug: 'workers',
    title: 'ผู้ปฏิบัติงาน',
    status: 'none',
    note: 'ไม่มีการบันทึกข้อมูล',
    ctaLabel: 'เพิ่มข้อมูล',
    image: '/images/workers.jpg',
    imageAlt: 'workers and laborers'
  }
]
