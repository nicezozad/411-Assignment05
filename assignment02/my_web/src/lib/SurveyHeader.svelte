<script>
  /** @type {{ passCount?: number, warnCount?: number, noneCount?: number }} */
  let { passCount = 0, warnCount = 0, noneCount = 0 } = $props()
</script>

<section class="header">
  <div class="stats">
    <div class="pill pass">ผ่าน {passCount}</div>
    <div class="pill warn">ต้องปรับปรุง {warnCount}</div>
    <div class="pill none">ยังไม่บันทึก {noneCount}</div>
  </div>
</section>

<style>
  .header { display:flex; align-items:center; gap:8px; padding:8px 0; }
  .stats { display:flex; gap:8px; }
  .pill { padding:6px 10px; border-radius:999px; font-size:12px; }
  .pass { background:#e8f7ee; color:#166534; }
  .warn { background:#fff4ed; color:#9a3412; }
  .none { background:#eef2ff; color:#3730a3; }
</style>
