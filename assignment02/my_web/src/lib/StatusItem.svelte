<script>
  /** @type {{
    slug: string,
    title: string,
    lastUpdated?: string,
    status?: 'pass'|'warn'|'none',
    note?: string,
    ctaLabel?: string,
    imageAlt?: string,
    image?: string          // เพิ่มพาธรูปแบบเว็บ
  }} */
  let {
    slug,
    title,
    lastUpdated = '',
    status = 'none',
    note = '',
    ctaLabel = 'ดูรายละเอียด',
    imageAlt = '',
    image = ''              
  } = $props()
</script>

<div class="card">
  <div class="item">
    {#if image}
      <img class="thumb" src={image} alt={imageAlt || title} />
    {:else}
      <div class="thumb placeholder"></div>
    {/if}
    <div class="content">
      <h3>{title}</h3>
      {#if lastUpdated}
        <p class="meta">บันทึกข้อมูลล่าสุด {lastUpdated}</p>
      {:else}
        <p class="meta">ยังไม่เคยบันทึกข้อมูล</p>
      {/if}
      <p class="status">
        <span class={`dot ${status}`}></span>
        {#if status === 'pass'}ผ่าน{:else if status === 'warn'}ต้องปรับปรุง{:else}ไม่มีการบันทึกข้อมูล{/if}
      </p>
      {#if note}<p class="note">{note}</p>{/if}
      <a class={`btn ${status}`} href={`/Status/${slug}`}>{ctaLabel}</a>
    </div>
  </div>
</div>

<style>
  .card { background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:14px; box-shadow:0 1px 2px rgba(0,0,0,.04) }
  .item { display:grid; grid-template-columns:112px 1fr; gap:14px; align-items:center }


  .thumb {
  width: 112px;
  height: 84px;
  border-radius: 12px;
  object-fit: cover;     
  border: 1px solid #e5e7eb;
  display: block;
  }
  .placeholder {
  background: #f3f4f6;
  }

  .content h3 { margin:0 0 4px; font-size:18px }
  .meta { margin:0 0 6px; color:#6b7280; font-size:13px }
  .status { margin:0 0 6px; font-weight:600; display:flex; align-items:center; gap:6px }
  .note { margin:0 0 10px; color:#374151; font-size:14px }
  .btn { display:inline-block; padding:8px 12px; border-radius:10px; text-decoration:none; font-weight:600; font-size:14px }
  .btn.pass { background:#e8f7ee; color:#166534 } .btn.warn { background:#ffe4e6; color:#9f1239 } .btn.none { background:#e5e7eb; color:#111827 }
  .dot { display:inline-block; width:10px; height:10px; border-radius:50%; vertical-align:middle }
  .dot.pass { background:#16a34a } .dot.warn { background:#ef4444 } .dot.none { background:#111827 }
</style>
