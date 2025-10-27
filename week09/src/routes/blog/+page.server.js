export async function load() {
  const url = 'https://jsonplaceholder.typicode.com/posts'

  //ป้องกัน error
  try {
    console.log('Fetching data from API')

    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`)
    }

    const posts = await response.json()
    console.log(`Fetching data succeed with ${posts.length} post(s)`)

    return {
      // @ts-ignore
      summaries: posts.map((post) => ({
        slug: post.id,
        title: post.title,
      }))
    }
  } catch (error) {
    // @ts-ignore
    console.error(error.message)
  }
}
