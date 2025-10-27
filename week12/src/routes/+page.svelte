<script>
    let { data } = $props()
</script>

<div class="centered">
    <h1>todos</h1>
    <form method="post">
        <label>
            add a todo:
            <input
                name="description"
                autocomplete="off"
            />
        </label>
    </form>
    <ul class="todos">
        {#each data.todos as todo (todo.id)}
            <li>
                {todo.description}
            </li>
        {/each}
    </ul>
</div>