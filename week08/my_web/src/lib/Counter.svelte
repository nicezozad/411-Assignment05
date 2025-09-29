<script>
    import { counter } from "$lib/Counter.svelte.js"
</script>

<button onclick={() => counter.count += 1}>
    clicks: {counter.count}
</button>

