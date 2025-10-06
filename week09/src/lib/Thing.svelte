<script>
    const emojis = {
        apple: '🍎',
        banana: '🍌',
        carrot: '🥕',
        doughnut: '🍩',
            egg: '🥚'
    }

    let { name } = $props()
    // @ts-ignore
    const emoji = emojis[name]
</script>

<p>{emoji} = {name}</p>