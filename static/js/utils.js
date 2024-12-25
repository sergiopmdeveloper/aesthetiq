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
