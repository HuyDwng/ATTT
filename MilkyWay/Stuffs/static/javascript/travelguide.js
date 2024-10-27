document.addEventListener('DOMContentLoaded', function(){
    // Select all category buttons
    const categoryButtons = document.querySelectorAll('.category');
    
    // Function to add 'active' class to clicked button and remove it from others
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove 'active' class from all buttons
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add 'active' class to the clicked button
            button.classList.add('active');
            updateImages(button.textContent);
        });
    });
    });
    
    const imageMap = {
        "Điểm đến phổ biến": [
            { src: "../static/images/bali.jpg", alt: "Popular Destination 1" },
            { src: "../static/images/DaNang.jpg", alt: "Popular Destination 2" },
            { src: "../static/images/france.jpg", alt: "Popular Destination 3" },
            { src: "../static/images/HaLong.jpg", alt: "Popular Destination 4" }
        ],
        "Trải nghiệm văn hóa": [
            { src: "../static/image/hanoi.jpg", alt: "Culture Experience 1" },
            { src: "../static/image/he.jpg", alt: "Culture Experience 2" },
            { src: "../static/image/hehehe.jpg", alt: "Culture Experience 3" },
            { src: "../static/image/japan.jpg", alt: "Culture Experience 4" }
        ],
        "Du lịch ẩm thực": [
            { src: "../static/image/logo.jpg", alt: "Food Destination 1" },
            { src: "../static/image/saigon.jpg", alt: "Food Destination 2" },
            { src: "../static/image/sapa.jpg", alt: "Food Destination 3" },
            { src: "../static/images/tfgj.jpg", alt: "Food Destination 4" }
        ],
        // Add more categories as needed
    };
    
    // Function to update images based on the selected category
    function updateImages(category) {
        const images = imageMap[category];
        const destinationCards = document.querySelectorAll('.destination-card');
    
        if (images) {
            destinationCards.forEach((card, index) => {
                const img = card.querySelector('.destination-image');
                img.src = images[index].src;
                img.alt = images[index].alt;
            });
        }
    }
    
    document.addEventListener('DOMContentLoaded', function(){
        // Select all category buttons
        const categoryButtons = document.querySelectorAll('.country');
        
        // Function to add 'active' class to clicked button and remove it from others
        categoryButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Remove 'active' class from all buttons
                categoryButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add 'active' class to the clicked button
                button.classList.add('active');
                updateImages(button.textContent);
            });
        });
        });
    
    