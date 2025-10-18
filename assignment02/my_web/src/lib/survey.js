/** @typedef {'pass'|'warn'|'none'} SurveyStatus */

/**
 * @typedef {Object} SurveyAspect
 * @property {string} slug
 * @property {string} title
 * @property {string=} lastUpdated
 * @property {SurveyStatus} status
 * @property {string=} note
 * @property {string=} ctaLabel
 * @property {string=} imageAlt
 */

/** @type {SurveyAspect[]} */
export const aspects = [
  { slug: 'water',       title: 'การจัดการน้ำ',      lastUpdated: '26/02/2568 เวลา 19:00 น.', status: 'warn', note: 'น้ำทิ้งยังมีโอกาสปนเปื้อน', ctaLabel: 'แก้ไขข้อมูล', imageAlt: 'water' },
  { slug: 'soil',        title: 'การจัดการที่ดิน',    lastUpdated: '26/02/2568 เวลา 19:00 น.', status: 'pass', note: 'แปลงเพาะปลูกเป็นตามมาตรฐาน', ctaLabel: 'ดูรายละเอียด', imageAlt: 'soil' },
  { slug: 'fert-chem',   title: 'การใช้ปุ๋ยและยา',    status: 'none', note: 'ไม่มีการบันทึกข้อมูล', ctaLabel: 'เพิ่มข้อมูล', imageAlt: 'fert-chem' },
  { slug: 'tools',       title: 'ยานพาหนะ อุปกรณ์',  status: 'none', note: 'ไม่มีการบันทึกข้อมูล', ctaLabel: 'เพิ่มข้อมูล', imageAlt: 'tools' },
  { slug: 'harvest',     title: 'การเก็บเกี่ยว',      status: 'none', note: 'ไม่มีการบันทึกข้อมูล', ctaLabel: 'เพิ่มข้อมูล', imageAlt: 'harvest' },
  { slug: 'postharvest', title: 'การพักผลผลิต',       status: 'none', note: 'ไม่มีการบันทึกข้อมูล', ctaLabel: 'เพิ่มข้อมูล', imageAlt: 'postharvest' },
  { slug: 'facilities',  title: 'สถานที่ต่าง ๆ',       status: 'none', note: 'ไม่มีการบันทึกข้อมูล', ctaLabel: 'เพิ่มข้อมูล', imageAlt: 'facilities' },
  { slug: 'workers',     title: 'ผู้ปฏิบัติงาน',       status: 'none', note: 'ไม่มีการบันทึกข้อมูล', ctaLabel: 'เพิ่มข้อมูล', imageAlt: 'workers' }
]
