/**
 * Disables the button that triggered the form submission.
 * @param {Event} event - The event that triggered the form submission.
 */
export function disableButtonOnLoading(event) {
  event.preventDefault();

  /** @type {HTMLButtonElement} */
  const button = event.target;

  const buttonVariant = button.getAttribute('variant');

  if (button) {
    button.disabled = true;

    const variantClassesToRemove = {
      primary: 'hover:bg-blue-700/80',
      destructive: 'hover:bg-red-700/80',
    };

    if (variantClassesToRemove[buttonVariant]) {
      button.classList.remove(variantClassesToRemove[buttonVariant]);
    }

    button.classList.add('opacity-50');
  }

  button.closest('form').submit();
}

window.disableButtonOnLoading = disableButtonOnLoading;

/**
 * Shows a toast message.
 * @param {string} id - The ID of the toast element.
 * @param {string} message - The message to show in the toast.
 */
export function showToast(id, message) {
  const toastRaw = `
    <div
      class="absolute bottom-4 right-4 flex items-center gap-2 bg-green-300 p-2 rounded-lg shadow"
      id="${id}"
    >
      <p class="text-green-700 text-xs">${message}</p>

      <button
        class="h-6 w-6 flex items-center justify-center bg-green-500 rounded-lg hover:bg-green-500/80 focus:ring-2 focus:ring-green-400"
        data-dismiss-target="#${id}"
      >
        <svg
          class="w-2 h-2 text-green-900"
          fill="none"
          viewBox="0 0 14 14"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
          />
        </svg>
      </button>
    </div>
  `;

  const tempContainer = document.createElement('div');
  tempContainer.innerHTML = toastRaw.trim();

  const toast = tempContainer.firstChild;

  setTimeout(() => {
    toast.remove();
  }, 3000);

  document.body.appendChild(toast);
}

window.showToast = showToast;
