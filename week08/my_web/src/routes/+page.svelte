<script>

    import Nice from "$lib/nice.svelte"
    import Mystate from "$lib/Mystate.svelte"
    import Counter from "$lib/Counter.svelte"
    import DeepState from "$lib/MyDeepState.svelte"
    import DerivedState from "$lib/MyDerivedState.svelte"
    let name = 'Yannapat Techai'
    let content = "this string contains some <strong>HTML!!!</strong>"
    let listsContent = '<ul> \
                        <li>Apple</li> \
                        <li>Banana</li> \
                        <li>Orange</li> \
                        <li>Graps</li> \
                        </ul>' 
</script>

<h1>Welcome to {name}</h1>

<Nice />
<Mystate />
<Counter />
<Counter />
<Counter />
<DeepState />
<DerivedState />


<p>YOOO</p>
<p>{@html content}</p>
<p>{@html listsContent}</p>

<style>
    h1,p {
        color: goldenrod;
        font-family: 'Comic Sans MS', cursive;
        font-size: 2em;
    }
</style>
