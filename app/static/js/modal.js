/**
 * Modal utility functions for Round Again application
 */

/**
 * Open the modal
 * @param {string} modalId - ID of the modal element
 */
function showModal(modalId = 'modal') {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('modal-open');
  }
}

/**
 * Close the modal
 * @param {string} modalId - ID of the modal element
 */
function hideModal(modalId = 'modal') {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('modal-open');
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
      hideModal(modalId);
    }
  });
  
  // Close modal when clicking outside of modal content
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.addEventListener('click', function(event) {
      if (event.target === modal) {
        hideModal(modalId);
      }
    });
  }
}

// Backward compatibility with old function names
const openModal = showModal;
const closeModal = hideModal;