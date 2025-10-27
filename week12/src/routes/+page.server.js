import * as db from '$lib/server/database.js'

// @ts-ignore
export function load({cookies}) {
    let id = cookies.get('userid')

    if (!id) {
        id = crypto.randomUUID()
        cookies.set('userid', id, {path: '/'})

        return {
            todos: db.getTodos(id)
        }
    }
}

export const actions = {
    // @ts-ignore
    dafault: async ({cookies, request}) => {
        db.createTodo(
            cookies.get('userid'),
            // @ts-ignore
            data.get('description')

        )
    }
}