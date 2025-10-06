<script>
	import favicon from '$lib/assets/favicon.svg'
	let { children } = $props()
</script>

<svelte:head>
	<link rel="icon" href={favicon} />

</svelte:head>
<nav>
	<a href="/">home</a>
	<a href="/blog">blog</a>
	<a href="/about">about</a>
	<a href="/ex02">ex02 + 03</a>
	<a href="/ex04">ex04</a>
	<a href="/ex05">ex05</a>
	
</nav>

{@render children()}