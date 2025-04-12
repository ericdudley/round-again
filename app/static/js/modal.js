/**
 * Modal utility functions for Round Again application
 */

/**
 * Open the modal
 * @param {string} modalId - ID of the modal element
 */
function openModal(modalId = 'modal') {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('hidden');
  }
}

/**
 * Close the modal
 * @param {string} modalId - ID of the modal element
 */
function closeModal(modalId = 'modal') {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('hidden');
  }
}

/**
 * Setup event listeners for modal closing
 * @param {string} modalId - ID of the modal element
 */
function setupModalListeners(modalId = 'modal') {
  // Close modal when escape key is pressed
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
      closeModal(modalId);
    }
  });
  
  // Close modal when clicking outside of modal content
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.addEventListener('click', function(event) {
      if (event.target === modal) {
        closeModal(modalId);
      }
    });
  }
}