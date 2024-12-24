/**
 * Disables the button that triggered the form submission.
 * @param {Event} event - The event that triggered the form submission.
 */
export function disableButtonOnLoading(event) {
  event.preventDefault();

  /** @type {HTMLButtonElement} */
  const button = event.target;

  if (button) {
    button.disabled = true;

    button.classList.remove('hover:bg-blue-700/80');
    button.classList.add('opacity-50');
  }

  button.closest('form').submit();
}

window.disableButtonOnLoading = disableButtonOnLoading;
