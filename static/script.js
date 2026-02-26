
function scrollToSection(event, sectionId)
{
    event.preventDefault();

    const element = document.getElementById(sectionId);
    if (element)
    {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

function openchat()
{
    let f = document.getElementById('ai-chat');
    if (f.classList.contains('close-chat'))
    {
        f.classList.remove('close-chat');
        f.classList.add('open-chat');
    }
    else
    {
        f.classList.add('close-chat');
        f.classList.remove('open-chat');
    }
}

let msgs = [];
function load_msgs()
{
    let messages = JSON.parse(localStorage.getItem("messages"));
    messages.forEach(([type, value]) => {
        console.log(type, value);
        msgs.push([type, value])
    });

    let ai_chat_ul = document.getElementById('ai-chat-ul');
    msgs.forEach(([type, value]) => {
        if (type === "usr")
        {
            let new_usr_msg = document.createElement('li');
            let usr_msg_ico = document.createElement('img');
            usr_msg_ico.src = "assets/user.svg";
            new_usr_msg.appendChild(usr_msg_ico);
            new_usr_msg.classList.add('usr-out');

            let new_usr_msg_p = document.createElement('p');
            new_usr_msg_p.innerText = value;
            new_usr_msg.appendChild(new_usr_msg_p);

            ai_chat_ul.appendChild(new_usr_msg);
        }
        else if (type === "ai")
        {
            let new_ai_msg = document.createElement('li');
            let ai_msg_ico = document.createElement('img');
            ai_msg_ico.src = "assets/robot.svg";
            new_ai_msg.appendChild(ai_msg_ico);
            new_ai_msg.classList.add('ai-out');

            let new_ai_msg_p = document.createElement('p');
            new_ai_msg_p.innerText = value;
            new_ai_msg.appendChild(new_ai_msg_p);

            ai_chat_ul.appendChild(new_ai_msg);
        }
    });
}
document.addEventListener("DOMContentLoaded", () => {
    load_msgs();

    let usr_ai_chat_inp = document.getElementById('ai-chat-input');
    usr_ai_chat_inp.addEventListener("keydown", (event) => {
        if (event.key === "Enter")
        {
            send_ai();
        }
    });
})

async function send_ai()
{
    // Adds the user message bubble to chat
    let usr_ai_chat_inp = document.getElementById('ai-chat-input');
    let ai_chat_ul = document.getElementById('ai-chat-ul');

    let new_usr_msg = document.createElement('li');
    new_usr_msg.classList.add('usr-out');

    let new_usr_msg_p = document.createElement('p');
    new_usr_msg_p.innerText = usr_ai_chat_inp.value;
    new_usr_msg.appendChild(new_usr_msg_p);

    ai_chat_ul.appendChild(new_usr_msg);
    msgs.push(["usr", usr_ai_chat_inp.value]);

    // Adds the AI message bubble to chat
    let new_ai_msg = document.createElement('li');
    let ai_msg_ico = document.createElement('img');
    ai_msg_ico.src = "assets/robot.svg";
    new_ai_msg.appendChild(ai_msg_ico);
    new_ai_msg.classList.add('ai-out');

    let new_ai_msg_p = document.createElement('p');
    new_ai_msg_p.innerText = "Loading...";
    new_ai_msg.appendChild(new_ai_msg_p);

    ai_chat_ul.appendChild(new_ai_msg);

    // Stores user input but clears the input box
    let usr_inp_value = usr_ai_chat_inp.value;
    usr_ai_chat_inp.value = "";

    // Sends it to the gpt api and gets the value
    const res = await axios.post("/gpt", {
        text: usr_inp_value,
        model: 'gpt-3.5-turbo'
    });
    const d = res.data.output;
    // Sets the message bubble to the value
    new_ai_msg_p.innerText = d;

    msgs.push(["ai", d]);

    localStorage.setItem("messages", JSON.stringify(msgs));
}