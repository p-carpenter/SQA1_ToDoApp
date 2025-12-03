document.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector('.tag-container');
    if (!container) return;

    const input = container.querySelector('input');

    const tags = [];

    container.querySelectorAll('.tag').forEach(tagEl => {
        const text = tagEl.textContent.trim().slice(0, -1); // remove ✖
        tags.push(text);

        const removeBtn = tagEl.querySelector('button');
        removeBtn.addEventListener('click', () => {
            const index = tags.indexOf(text);
            removeTag(index);
        });
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            addTag(input.value);
        } else if (e.key === 'Backspace' && input.value === '' && tags.length > 0) {
            removeTag(tags.length - 1);
        }
    });

    const addTag = (text) => {
        if (!text || tags.includes(text)) {
            input.value = '';
            return;
        }

        tags.push(text);

        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.innerHTML = `${text} <button type='button'>✖</button>`;

        const removeBtn = tag.querySelector('button');
        removeBtn.addEventListener('click', () => {
            const index = tags.indexOf(text);
            removeTag(index);
        });

        container.insertBefore(tag, input);
        input.value = '';
    };

    const removeTag = (index) => {
        tags.splice(index, 1);
        const tagElements = container.querySelectorAll('.tag');
        tagElements[index].remove();
    };

    const form = container.closest("form");
    const hiddenInput = document.getElementById("hidden-tags");

    form.addEventListener("submit", () => {
        // so that tags are submitted correctly
        hiddenInput.value = tags.join(",");
    });

});
