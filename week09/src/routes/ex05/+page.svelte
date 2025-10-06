<script>
    import Stepper from '$lib/Stepper.svelte'

    let value = $state(0)
</script>

<p>The current value is {value}</p>

<Stepper
    increment1={() => value += 1}
    decrement1={() => value -= 1}

    increment2={() => value += 2}
    decrement2={() => value -= 2}

    increment3={() => value += 3}
    decrement3={() => value -= 3}

    increment4={() => value += 4}
    decrement4={() => value -= 4}
/>
