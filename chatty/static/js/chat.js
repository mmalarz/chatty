let chatWindow = document.getElementById('chat-window');
let chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

// scroll to bottom at start
chatWindow.scrollTop = chatWindow.scrollHeight;

handleMessageForm();

chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    let message = data['message'];
    let users = data['users'];

    if (message) {
        displayMessage(data, message);
    }
    else if (users) {
        displayActiveUsers(users);
    }
};

chatSocket.onclose = function (e) {
    chatSocket.close();
};

function handleMessageForm() {
    document.getElementById('chat-message-input').focus();
    document.getElementById('chat-message-input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.forms['chat-form'].submit();
        }
    };
    document.getElementById('chat-message-submit').onclick = function (e) {
        let messageInput = document.querySelector('#chat-message-input');
        let message = messageInput.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInput.value = '';
    };
}

function displayMessage(data, message) {
    let messageUsername = data['username'];
    let messageUserFirstName = data['first_name'];
    let messageUserLastName = data['last_name'];
    let ul = document.getElementById('chat-window');
    let li = document.createElement('li');
    let clearDiv = document.createElement('div');

    li.innerHTML = message;
    clearDiv.style.clear = 'both';

    // check from who is the message to style it properly
    if (activeUsername === messageUsername) {
        li.className = 'chat-user-message';
    } else {
        li.className = 'chat-others-message';
        let pTagName = document.createElement('p');

        pTagName.className = 'message-username';
        pTagName.innerHTML = messageUserFirstName + ' ' + messageUserLastName;
        ul.appendChild(pTagName);
    }
    ul.appendChild(li);
    ul.appendChild(clearDiv);

    // scroll to bottom after sending new message
    let element = document.getElementById('chat-window');
    element.scrollTop = element.scrollHeight;
}

function displayActiveUsers(users) {
    users = users[roomName];
    let userList = document.getElementById('user-list');
    userList.innerHTML = '';

    for (let i = 0; i < users.length; i++) {
        let userDiv = document.createElement('div');
        userDiv.innerHTML = users[i];
        userDiv.className = 'collection-item';
        userList.appendChild(userDiv);
    }
}