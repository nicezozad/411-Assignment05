<script>
  let { children } = $props()
</script>

<nav class="nav">
  <a href="/">home</a>
  <a href="/blog">blog</a>
  <a href="/about">about</a>
  <a href="/Survey">สำรวจเพาะปลูก 8 ด้าน</a>
  <a href="/reports">reports</a>
  <a href="/settings">settings</a>
</nav>

{@render children()}

<style>
  .nav {
    display: flex;
    gap: 12px;
    padding: 12px 16px;
    border-bottom: 1px solid #eee;
  }
  .nav a {
    text-decoration: none;
    color: #333;
  }
  .nav a:hover {
    text-decoration: underline;
  }
</style>
