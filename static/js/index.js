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
    const formData = new FormData(form);

    try
    {
	    const response = await fetch(`${window.location.origin}/get_files`,
	    {
	        method: "POST",
	        body: formData,
	    });

	    archive = await response.json();

		const card_list = document.querySelector(".card-list");
		const cards = card_list.querySelectorAll(".card-container");
		cards.forEach(card => card.remove());

		archive.files.forEach(filename => {
    		make_cardElement(filename);
		});
    }
    catch (e)
    {
        console.error(e);
    }
}

const form = document.querySelector(".form-input");

form.addEventListener("submit", (event) => {
    event.preventDefault();
    sendData();
});


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

document.addEventListener("DOMContentLoaded", async () => {
    try
    {
        const response = await fetch("/get_files");
        const archive = await response.json();

        archive.files.forEach(filename => {
            make_cardElement(filename);
        });

    }
    catch (error)
    {
        console.error(error);
    }
});
