/*
 * Name    : statScript.js
 * Author  : Tygan Chin
 * Purpose : Allow user to interact with player report screen
 */

currCarreerStat = 0;
const careerStats = [
    [document.getElementById('careerPPGbutton'), document.getElementById('careerPts')], 
    [document.getElementById('careerRPGbutton'), document.getElementById('careerRebs')],
    [document.getElementById('careerAPGbutton'), document.getElementById('careerAsts')],
    [document.getElementById('careerSPGbutton'), document.getElementById('careerStls')],
    [document.getElementById('careerBPGbutton'), document.getElementById('careerBlks')],
    [document.getElementById('careerMPGbutton'), document.getElementById('careerMins')],
    [document.getElementById('careerTPGbutton'), document.getElementById('careerTovs')]]

function countingStatButtonClicked(buttonInd) {
    /* hide previous graph and button */
    careerStats[currCarreerStat][0].style.textDecoration = 'none'
    careerStats[currCarreerStat][1].style.display = 'none'

    /* display new graph and button */
    careerStats[buttonInd][0].style.textDecoration = 'underline'
    careerStats[buttonInd][1].style.display = 'flex'

    /* set curr index */
    currCarreerStat = buttonInd
}

currAverage = 0;
const careerAvgs = [
    [document.getElementById('careeraverages-button'), document.getElementById('careerAverages')], 
    [document.getElementById('playoffaverages-button'), document.getElementById('playoffAverages')],
    [document.getElementById('currentaverages-button'), document.getElementById('currentAverages')]]

function averagesButtonClicked(buttonInd) {
    /* hide previous graph and button */
    careerAvgs[currAverage][0].style.textDecoration = 'none'
    careerAvgs[currAverage][1].style.display = 'none'

    /* display new graph and button */
    careerAvgs[buttonInd][0].style.textDecoration = 'underline'
    careerAvgs[buttonInd][1].style.display = 'grid'

    /* set curr index */
    currAverage = buttonInd
}

currTotal = 0;
const careerTotals = [
    [document.getElementById('totalCareerPts_button'), document.getElementById('totalCareerPts')], 
    [document.getElementById('totalCareerRebs_button'), document.getElementById('totalCareerRebs')],
    [document.getElementById('totalCareerAsts_button'), document.getElementById('totalCareerAsts')],
    [document.getElementById('totalCareerStls_button'), document.getElementById('totalCareerStls')],
    [document.getElementById('totalCareerBlks_button'), document.getElementById('totalCareerBlks')],
    [document.getElementById('totalCareerTovs_button'), document.getElementById('totalCareerTovs')]]

function totalStatButtonClicked(buttonInd) {
    /* hide previous graph and button */
    careerTotals[currTotal][0].style.textDecoration = 'none'
    careerTotals[currTotal][1].style.display = 'none'

    /* display new graph and button */
    careerTotals[buttonInd][0].style.textDecoration = 'underline'
    careerTotals[buttonInd][1].style.display = 'flex'

    /* set curr index */
    currTotal = buttonInd
}

function goHome() {
    window.location.href = "/";
}

/* search functionality */
fetch('static/data/players.json') 
    .then(response => response.json())
    .then(data => {

        playerList = data;
        topBar = document.getElementById('top-bar')
        main = document.getElementById('main')
        footer = document.getElementById('footer')
        body = document.getElementById('body')
        loading = document.getElementById('loading')
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
    
            /* click */
            result.addEventListener('click', () => {
                console.log(playerList[i]['id'])
                topBar.style.display = 'none'
                main.style.display = 'none'
                footer.style.display = 'none'
                body.style.backgroundColor = main.style.backgroundColor
                loading.style.display = 'flex'
                window.location.href = `http://127.0.0.1:5000/submit?id=${playerList[i]['id']}`;
            })
    
            resultsContainer.append(result)
        }
        resultsContainer.lastElementChild.style.borderBottom = 'none'
    
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
        
        resultsContainer = document.getElementById('results-container')
        input.addEventListener('focus', () => {
            resultsContainer.style.display = 'flex'
            input.style.borderBottomLeftRadius = '0px'
            input.style.borderBottomRightRadius = '0px'
        });
        
        input.addEventListener('blur', function(event) {
            setTimeout(() => {
                resultsContainer.style.display = 'none';
                input.style.borderBottomLeftRadius = '1vw';
                input.style.borderBottomRightRadius = '1vw';
            }, 100);
        });
        
    })
    .catch(error => console.error('Error loading JSON:', error));