const db = new Map()

// @ts-ignore
export function getTodos(userid) {
  if (!db.get(userid)) {
    db.set(userid, [
      {
        id: crypto.randomUUID(),
        description: 'Learn SvelteKit',
        done: false,
      },
    ])
  }
  return db.get(userid)
}

// @ts-ignore
export function createTodo(userid, description) {
  const todos = db.get(userid)
  todos.push({
    id: crypto.randomUUID(),
    description,
    done: false,
  })
}

// @ts-ignore
export function deleteTodo(userid, todoid) {
  const todos = db.get(userid)
  // @ts-ignore
  const index = todos.findIndex((todo) => todo.id === todoid)
  if (index !== -1) {
    todos.splice(index, 1)
  }
}
