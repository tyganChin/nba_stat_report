/*
 * Name    : home.js
 * Author  : Tygan Chin
 * Purpose : Create search box for all NBA players and send request for report 
 *           when player is pressed
 */

/* read in the player json file */
fetch('static/data/players.json')
  .then(response => response.json())
  .then(data => {

    /* get player list */
    playerList = data;

    container = document.getElementById('container')
    loadingScreen = document.getElementById('loading')

    /* add all players to search result container */
    container.style.display = 'flex'
    loadingScreen.style.display = 'none'
    resultsContainer = document.getElementById('results-container')
    for (let i = 0; i < playerList.length; ++i) {
        const result = document.createElement('div');
        result.classList = 'result'

        const imgContainer = document.createElement('div');
        imgContainer.classList = 'result-img';
        const img = document.createElement('img');
        img.src = 'https://cdn.nba.com/headshots/nba/latest/1040x760/' + playerList[i]['id'] + '.png'
        imgContainer.append(img)
        result.append(imgContainer)

        const name = document.createElement('div');
        name.classList = 'result-name';
        name.innerHTML = playerList[i]['full_name']
        result.append(name)

        /* send request for next player report on click */
        result.addEventListener('click', () => {
            console.log(playerList[i]['id'])
            container.style.display = 'none'
            loadingScreen.style.display = 'flex'
            window.location.href = `http://127.0.0.1:5000/submit?id=${playerList[i]['id']}`;
        })

        resultsContainer.append(result)
    }
    resultsContainer.lastElementChild.style.borderBottom = 'none'

    /* search box feature */
    inputBox = document.getElementById('input')
    const elements = resultsContainer.querySelectorAll('.result');
    inputBox.addEventListener('input', () => {
        inputSize = inputBox.value.length
        elements.forEach(element => {
            names = element.textContent.split(' ')
            last = "";
            if (names.length > 1) {
                last = names[names.length - 1]
                console.log(last)
            }
            if (inputBox.value == element.textContent.slice(0, inputSize).toLowerCase() || inputBox.value == last.slice(0, inputSize).toLowerCase()) {
                element.style.display = 'flex'
            } else {
                element.style.display = 'none'
            }
        });
    })

    /* display search result box when search box is clicked */
    input.addEventListener('focus', () => {
        resultsContainer.style.display = 'flex'
        input.style.borderBottomLeftRadius = '0px'
        input.style.borderBottomRightRadius = '0px'
    });

    /* hide search result box when clicked off */
    input.addEventListener('blur', function(event) {
        setTimeout(() => {
            resultsContainer.style.display = 'none';
            input.style.borderBottomLeftRadius = '1vw';
            input.style.borderBottomRightRadius = '1vw';
        }, 100);
    });
})
.catch(error => console.error('Error loading JSON:', error));
