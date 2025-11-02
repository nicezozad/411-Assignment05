import { aspects } from './aspects.js'

/**
 * @typedef {Object} Farmer
 * @property {string} id
 * @property {string} name
 * @property {string} area
 * @property {SurveyAspect[]} surveys
 */

/** @type {Farmer[]} */
export const farmers = [
  {
    id: 'F001',
    name: 'นายสมชาย ใจดี',
    area: 'เชียงใหม่',
    surveys: aspects.map(a =>
      a.category === 'water' || a.category === 'soil'
        ? { ...a, note: 'บันทึกข้อมูลแล้ว', ctaLabel: 'แก้ไขข้อมูล' }
        : { ...a, note: 'ยังไม่มีการบันทึก', ctaLabel: 'เพิ่มข้อมูล' }
    )
  },
  {
    id: 'F002',
    name: 'นางสาวกัญญา แสงทอง',
    area: 'ลพบุรี',
    surveys: aspects.map(a =>
      a.category === 'fert-chem'
        ? { ...a, note: 'บันทึกข้อมูลแล้ว', ctaLabel: 'แก้ไขข้อมูล' }
        : { ...a, note: 'ยังไม่มีการบันทึก', ctaLabel: 'เพิ่มข้อมูล' }
    )
  },
  {
    id: 'F003',
    name: 'นายธีรภัทร วิชัย',
    area: 'นครปฐม',
    surveys: aspects.map(a =>
      ({ ...a, note: 'ยังไม่มีการบันทึก', ctaLabel: 'เพิ่มข้อมูล' }))
  }
]
