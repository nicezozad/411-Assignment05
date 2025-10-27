import { error } from '@sveltejs/kit'

// @ts-ignore
export async function load({ params }) {
  const url = `https://jsonplaceholder.typicode.com/posts/${params.slug}`

  try {
    console.log(`Fetching data from API ${url}`)

    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`)
    }

    console.log(`Fetching data succeed with ${response.status}`)

    const data = await response.json()
    if (!data) error(404)

    const post = {
      title: data.title,
      content: data.body,
    }

    return {
      post,
    }
  } catch (error) {
    // @ts-ignore
    console.error(error.message)
  }
}
