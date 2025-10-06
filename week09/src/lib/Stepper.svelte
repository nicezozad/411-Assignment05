<script>
    let { increment1, decrement1,increment2, decrement2 ,increment3, decrement3,increment4, decrement4 } = $props()
</script>

<button onclick={decrement1}>-1</button>
<button onclick={increment1}>+1</button>

<button onclick={decrement2}>-2</button>
<button onclick={increment2}>+2</button>

<button onclick={decrement3}>-3</button>
<button onclick={increment3}>+3</button>

<button onclick={decrement4}>-4</button>
<button onclick={increment4}>+4</button>