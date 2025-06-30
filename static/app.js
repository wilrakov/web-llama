document.addEventListener('DOMContentLoaded', () => {
    const ui = {
        // ... (tous les éléments de l'interface)
        uploadBtn: document.getElementById('upload-btn'),
        fileInput: document.getElementById('file-input'),
        deleteConvBtn: document.getElementById('delete-conv-btn'),
    };

    // ... (init et autres fonctions)

    function init() {
        // ...
        ui.uploadBtn.addEventListener('click', uploadFiles);
        ui.deleteConvBtn.addEventListener('click', deleteCurrentConversation);
    }

    // --- Conversations ---
    async function deleteCurrentConversation() {
        if (!currentConversationId) return;
        if (confirm("Êtes-vous sûr de vouloir supprimer cette conversation ?")) {
            await fetch(`/api/conversations/${currentConversationId}`, { method: 'DELETE' });
            document.querySelector(`#history-list li[data-id='${currentConversationId}']`).remove();
            createNewConversation();
        }
    }

    // --- Upload ---
    async function uploadFiles() {
        // ... (Logique d'upload restaurée)
    }

    // ... (le reste du code)
});