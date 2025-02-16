//My code is crap but is my code

const form = document.querySelector(".form-input");

form.addEventListener("submit", (event) => {
    event.preventDefault();
    sendData();
});

function uploadFile()
{
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (file)
    {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success)
            {
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

async function sendData()
{
    const search = new FormData(form);

    try
    {
	    const response = await fetch(`${window.location.origin}/get_files/1`,
	    {
	        method: "POST",
	        body: search,
	    });

	    archive = await response.json();

		const card_list = document.querySelector(".card-list");
		const cards = card_list.querySelectorAll(".card-container");
		cards.forEach(card => card.remove());
		// Loaded from search
		archive.files.forEach(filename => {
    		make_cardElement(filename);
		});
		make_paginationSection(archive.chunks);
    }
    catch (e)
    {
        console.error(e);
    }
}

function make_cardElement(filename)
{

	const cardList = document.querySelector(".card-list");

	const card_container = document.createElement("div");
	card_container.classList.add("card-container");

	const card = document.createElement("a");
	card.classList.add("card");

	const card_tittle = document.createElement("div");
	card_tittle.classList.add("card-title");
	card_tittle.innerText = filename;

	if(filename.includes('.pdf'))
	{
		const img = document.createElement("img");

		img.classList.add("card-thumbnail");
		img.src = `thumbnail/${filename.replace(".pdf", ".webp")}`;

		card.append(img);
		card.href = `view_pdf/${filename}`;
	}

	if(filename.includes('.md'))
	{
		const iframe = document.createElement("iframe");

		iframe.classList.add("card-thumbnail")
		iframe.src = `view_md/${filename}`;
		iframe.scrolling = "no";

		card.append(iframe);
		card.href = `view_md/${filename}`;
	}

	card_container.append(card);
	card.append(card_tittle);
	cardList.append(card_container);
}

function make_paginationSection(n_button)
{
	const pagination_section = document.querySelector(".pagination-section");
	pagination_section.innerHTML = "";
	top_button = (n_button <= 5) ? n_button : 5
	
	for(var i = 0; i < top_button; i++){
		let button = document.createElement("button");
		button.innerText = i + 1;
		button.classList.add("pagination-button");
		button.addEventListener("click", function() {
   			 button_event(this);
		});
		pagination_section.append(button);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    try
    {
        const response = await fetch(`/get_files/1`);
        const archive = await response.json();
		//Loaded from all
        archive.files.forEach(filename => {
            make_cardElement(filename);
        });
		make_paginationSection(archive.chunks);
    }
    catch (error)
    {
        console.error(error);
    }
});

async function button_event(e) {
    const input_search = document.querySelector(".input-search");
    let response;
    try {
        if (input_search.value) {
            response = await fetch(`${window.location.origin}/get_files/${e.innerText}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `query=${input_search.value}`,
            });
        } else {
            response = await fetch(`/get_files/${e.innerText}`);
        }

        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        const archive = await response.json();

        const card_list = document.querySelector(".card-list");
        const cards = card_list.querySelectorAll(".card-container");

        cards.forEach(card => card.remove());

        archive.files.forEach(filename => {
            make_cardElement(filename);
        });

    } catch (error) {
        console.error("Error:", error);
    }
}
