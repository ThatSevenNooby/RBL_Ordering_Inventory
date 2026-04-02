document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('addProductModal');
    const form = document.getElementById('addProductForm');
    const modalTitle = form.querySelector('h2');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const addBtn = document.getElementById('openFormBtn');
    const editBtns = document.querySelectorAll('.editBtn');

    addBtn.addEventListener('click', () => {
        form.reset();
        modalTitle.textContent = "Add New Product";
        submitBtn.textContent = "Save Product";
        form.action = ""; 
        document.getElementById('image').required = false; 
        modal.showModal();
    });

    editBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            document.getElementById('product_name').value = this.getAttribute('data-name');
            document.getElementById('category_id').value = this.getAttribute('data-category');
            document.getElementById('brand_id').value = this.getAttribute('data-brand');
            document.getElementById('price').value = this.getAttribute('data-price');
            document.getElementById('quantity').value = this.getAttribute('data-qty');
            document.getElementById('description').value = this.getAttribute('data-desc');
            modalTitle.textContent = "Edit Product";
            submitBtn.textContent = "Update Product";
            document.getElementById('image').required = false;
            form.action = `/dashboard/products/edit/${id}/`;

            modal.showModal();
        });
    });
    cancelBtn.addEventListener('click', () => {
        modal.close();
        form.reset();
    });
});