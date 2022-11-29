let users = {
};

let previousIds = [
  null,
];

function calculateRelativeDate(date) {
  let relativeDate = (Date.now() - date) / 1000;

  const units = [
    ['seconde', 60],
    ['minute', 60],
    ['heure', 24],
    ['jour', (365.25 / 12)],
    ['mois', 12], // Jusqu'a ce que je trouve mieux :shrug:
    // Peu utile de toute facon, Opacq est suppose etre ephemere
    ['annee', Infinity],
  ];

  // [unit, timeReqForNextUnit]

  let bestUnit;

  for (let index = 0; index < units.length; index++) {
    const [unit, time] = units[index];
    if (relativeDate / time <= 1) {
      bestUnit = unit;
      break;
    } else {
      relativeDate /= time;
    }
  }

  return `Il y a ${Math.floor(relativeDate)} ${bestUnit}${bestUnit.endsWith('s') || relativeDate < 2 ? '' : 's'}`
}

const components = {
  memberCard(id, name, pfp, isMe) {
    const cardElm = document.createElement('div');
    cardElm.classList.add('member_card', isMe ? 'surface' : 'you');
    cardElm.onclick = (event) => createTab(id, name, pfp);

      const pfpElm = document.createElement('div');
      pfpElm.classList.add('pfp');
      pfpElm.textContent = pfp;
      
      const nameElm = document.createElement('b');
      nameElm.classList.add('name');
      nameElm.textContent = name;

    cardElm.append(pfpElm, nameElm);
    return cardElm;
  },
  tab(id, name, pfp) {
    const tabElm = document.createElement('div');
    tabElm.classList.add('member', 'tab');
    tabElm.onclick = (event) => switchToTab(id);
    tabElm.dataset.id = id;

      const pfpElm = document.createElement('div');
      pfpElm.classList.add('pfp');
      pfpElm.textContent = pfp;
      
      const nameElm = document.createElement('b');
      nameElm.textContent = name;
      
      const closeElm = document.createElement('div');
      closeElm.onclick = (event) => {
        event.stopPropagation();
        closeTab(id);
      };

        const closeImgElm = document.createElement('img');
        closeImgElm.alt = 'Close';
        closeImgElm.src = 'close.png';

      closeElm.append(closeImgElm);

    tabElm.append(pfpElm, nameElm, closeElm);
    return tabElm;
  },
  frame(id) {
    const frameElm = document.createElement('div');
    frameElm.classList.add('frame', 'chat_pane');
    frameElm.dataset.id = id;

      const chatsElm = document.createElement('div');
      chatsElm.classList.add('chats', 'scrollbar');
      
      const inputElm = document.createElement('div');
      inputElm.classList.add('chat_input');

        const inputContainerElm = document.createElement('div');
        inputContainerElm.classList.add('chat_container', 'surface');

          const inputSendElm = document.createElement('div');
          inputSendElm.classList.add('pfp');

            const sendImgElm = document.createElement('img');
            sendImgElm.alt = 'Send';
            sendImgElm.src = 'send.png';

          inputSendElm.append(sendImgElm);

          const inputContentElm = document.createElement('pre');
          inputContentElm.classList.add('scrollbar');
          inputContentElm.contentEditable = true;

        inputContainerElm.append(inputSendElm, inputContentElm);

      inputElm.append(inputContainerElm);

    frameElm.append(chatsElm, inputElm);
    return frameElm;
  },
  chat(sender, chat, pfp) {
    const chatContainerElm = document.createElement('div');
    chatContainerElm.classList.add('chat_container', sender);

      const chatSenderElm = document.createElement('div');
      chatSenderElm.classList.add('pfp');
      chatSenderElm.textContent = pfp;

      const chatElm = document.createElement('div');
      chatElm.classList.add('chat');

        const chatContentsElm = document.createElement('div');
        chatContentsElm.classList.add('contents');
        chatContentsElm.textContent = chat;

        const chatDateElm = document.createElement('div');
        chatDateElm.classList.add('date');
        chatDateElm.textContent = 'Maintenant';

        const date = Date.now();

        setTimeout(() => {
          chatDateElm.textContent = calculateRelativeDate(date);

          setInterval(() => {
            chatDateElm.textContent = calculateRelativeDate(date);
          }, 5000);
        }, 60000)

      chatElm.append(chatContentsElm, chatDateElm);

    chatContainerElm.append(chatSenderElm, chatElm);
    return chatContainerElm;
  },
};

function switchToTab(id) {
  console.log(id)

  document
    .querySelector('.tab.current')
    .classList.remove('current');
  document
    .querySelector('.frame.current')
    .classList.remove('current');

  if (id == null) {
    document
      .querySelector('.tab.plus_icon')
      .classList.add('current');

    document
      .querySelector('.frame.new_member')
      .classList.add('current');
  } else {
    document
      .querySelector(`.tab[data-id="${id}"]`)
      .classList.add('current');

    document
      .querySelector(`.frame[data-id="${id}"]`)
      .classList.add('current');

    // Push to previousIds and filter it for duplicates
    previousIds = [...previousIds, id].filter((value, index, self) => self.indexOf(value) === index);
  }
}

function closeTab(id) {
  previousIds = previousIds.filter((v) => v !== id);
  switchToTab(previousIds[previousIds.length - 1]);
  const tabElm = document
    .querySelector(`.tab[data-id="${id}"]`);

  tabElm.parentElement.removeChild(tabElm);

  const frameElm = document
    .querySelector(`.frame[data-id="${id}"]`);

  frameElm.parentElement.removeChild(frameElm);
}

function createTab(id) {
  document.querySelector('.plus_icon')
    .before(components.tab(id, users[id].name, users[id].pfp));
  document.querySelector('main')
    .append(components.frame(id));
  switchToTab(id);
}

function addUser(id, isMe) {
  if (isMe) {
    document.querySelector('.who_am_i')
      .append(components.memberCard(id, users[id].name, users[id].pfp, true));
  } else {
    document.querySelector('.member_panel')
      .append(components.memberCard(id, users[id].name, users[id].pfp, false));
  }
}

function createMessage(id, sender, content) {
  document
    .querySelector(`.frame[data-id="${id}"] .chats`)
    .prepend(components.chat(sender, content, users[id].pfp));
}

require('electron').ipcRenderer.on('NEW_MEMBER', (event, message) => {
  users[message.id] = {
    name: message.name,
    pfp: message.pfp,
  };
  addUser(message.id, message.me);
})
