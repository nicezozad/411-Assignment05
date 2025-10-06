<script>
import YourComponent from '$lib/YourComponent.svelte'

const pkg = { 
    name: 'svelte',
    version: 5,
    description: 'blazing fast',
    website: 'https://svelte.dev'
}
</script>

<YourComponent {...pkg} />