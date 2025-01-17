const fileItems = [
    { name: 'My Folder', type: 'folder', icon: 'fas fa-folder' },
    { name: 'My Document.docx', type: 'document', icon: 'fas fa-file-word' },
    // ... more file items
];

const fileList = document.querySelector('.file-list');

fileItems.forEach(item => {
    const fileItem = document.createElement('div');
    fileItem.classList.add('file-item');
    fileItem.innerHTML = `
        <i class="${item.icon}"></i> 
        <span>${item.name}</span>
    `;
    fileList.appendChild(fileItem);
});