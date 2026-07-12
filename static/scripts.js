document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('task-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const title = document.getElementById('task-title').value;

            // Verifica se a tarefa já está sendo processada
            if (form.hasAttribute('data-submitting')) {
                return;
            }

            form.setAttribute('data-submitting', 'true');

            fetch('/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title }),
            })
            .then(response => response.json())
            .then(data => {
                alert('Tarefa adicionada!');
                document.getElementById('task-title').value = '';
            })
            .catch(error => console.error('Erro:', error))
            .finally(() => {
                form.removeAttribute('data-submitting');
            });
        });
    }

    document.querySelectorAll('.task-title').forEach(input => {
        input.addEventListener('change', () => {
            const id = input.getAttribute('data-id');
            const title = input.value;
            const done = input.nextElementSibling.checked;
            updateTask(id, { title, done });
        });
    });

    document.querySelectorAll('.task-done').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const id = checkbox.getAttribute('data-id');
            const title = checkbox.previousElementSibling.value;
            const done = checkbox.checked;
            updateTask(id, { title, done });
        });
    });
});

function updateTask(id, updates) {
    fetch(`/tasks/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates),
    })
    .then(response => response.json())
    .then(data => {
        alert('Tarefa atualizada!');
    })
    .catch(error => console.error('Erro:', error));
}

function deleteTask(id) {
    fetch(`/tasks/${id}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(`task-${id}`).remove();
        alert('Tarefa deletada!');
    })
    .catch(error => console.error('Erro:', error));
}
