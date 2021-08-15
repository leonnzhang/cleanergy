window.onload = () => {
    const modal = document.getElementById('resModal');
    const close = document.getElementById('modalClose');

    const mCost = document.getElementById('modal-cost');
    const mEnergy = document.getElementById('modal-energy');
    const mEmis = document.getElementById('modal-emissions');

    const mFact1 = document.getElementById('modal-fact1');
    const mFact2 = document.getElementById('modal-fact2');
    const mFact3 = document.getElementById('modal-fact3');
    const mFact4 = document.getElementById('modal-fact4');

    // non renewables
    // sorry judges for the very terrible code. ran out of time so we ended up throwing it all together like this...
    document.getElementById('coalSubmit').addEventListener('click', () => {
        let info = coal(document.getElementById('coal-count').value);
        let fact = factsCalc(info[1], info[2]);

        fillModal(info[0], info[1], info[2], fact[0], fact[1], fact[2], fact[3]);
    });
    document.getElementById('oilSubmit').addEventListener('click', () => {
        let info = oil(document.getElementById('oil-count').value, document.getElementById('crude').checked ? 'crude': 'gasoline');
        let fact = factsCalc(info[1], info[2]);

        fillModal(info[0], info[1], info[2], fact[0], fact[1], fact[2], fact[3]);
    });
    document.getElementById('gasSubmit').addEventListener('click', () => {
        let info = coal(document.getElementById('gas-count').value);
        let fact = factsCalc(info[1], info[2]);

        fillModal(info[0], info[1], info[2], fact[0], fact[1], fact[2], fact[3]);
    });

    // renewables
    document.getElementById('solarSubmit').addEventListener('click', () => {
        let info = solar(document.getElementById('solar-count').value, document.getElementById('solar-wattage').value, document.getElementById('solar-hours').value);
        let fact = factsCalc(info[1], info[2]);

        fillModal(info[0], info[1], 0, fact[0], fact[1], fact[2], fact[3], 'r');
    });
    document.getElementById('windSubmit').addEventListener('click', () => {
        let info = solar(document.getElementById('wind-count').value, document.getElementById('wind-blades').value, document.getElementById('wind-speed').value);
        let fact = factsCalc(info[1], info[2]);

        fillModal(info[0], info[1], 0, fact[0], fact[1], fact[2], fact[3], 'r');
    })
    document.getElementById('hydroSubmit').addEventListener('click', () => {
        let info = solar(document.getElementById('hydro-count').value, document.getElementById('hydro-length').value, document.getElementById('hydro-eff').value);
        let fact = factsCalc(info[1], info[2]);

        fillModal(info[0], info[1], 0, fact[0], fact[1], fact[2], fact[3], 'r');
    })

    // modal close
    close.onclick = () => {
        modal.style.display = 'none';
    }
    window.onclick = (event) => {
        if(event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // modifies/populates modal with info, simple split replace
    // my brain is fried so this will have to do...
    function fillModal(c, e, emis, f1, f2, f3, f4, type) {
        if(type == 'r') {
            mCost.innerText = mCost.innerText.split('$')[0] + `$${c.toFixed(2)} to install.`
            // it gets worse...
            mEmis.style.display = 'none';

            mFact3.style.display = 'none';
            mFact4.style.display = 'none';
        } else {
            mCost.innerText = mCost.innerText.split('$')[0] + `$${c.toFixed(2)} to burn everyday.`
            mEmis.innerText = mEmis.innerText.split(' emit')[0] + ` emit ${emis.toFixed(2)} kilograms of carbon dioxide per day.`


            mEmis.style.display = 'block';

            mFact3.style.display = 'block';
            mFact4.style.display = 'block';
            mFact3.innerText = mFact3.innerText.split(' for')[0] + ` for ${f3.toFixed(2)} kilometers.`
            mFact4.innerText = mFact4.innerText.split(' take')[0] + ` take ${f4.toFixed(2)} trees to offset the daily emissions.`
        }

        mEnergy.innerText = mEnergy.innerText.split(' generate')[0] + ` generate ${e.toFixed(2)/1000} kilowatt-hours per day.`
        
        // facts
        mFact1.innerText = mFact1.innerText.split(' for')[0] + ` for ${f1.toFixed(2)} hours.`
        mFact2.innerText = mFact2.innerText.split(' for')[0] + ` for ${f2.toFixed(2)} days.`
    
        modal.style.display = 'block';
    }
}

function factsCalc(energy, em) {
    return [energy/234, energy/3000, em*4.6, em/0.06]
}


/* big brain maths */
function solar(x, y, z) {
    let cost = 650*x;
    let energy = 24*x*y*z;
    return [cost, energy]
}

function wind(x, y, z) {
    let cost = 4000000*x;
    let energy = 18.1 * (y**2) * (z**3) * x;
    return [cost, energy]
}

function hydro(x, y, z) {
    z/=3.6; /* converts km/h --> m/s*/
    z/= 100;
    let energy = 212 * x * y * z;
    let cost = energy/12;
    return [cost, energy]
}

function coal(x) {
    let cost = 0.15*x;
    let emission = 2.11*x;
    let energy = 6000*x;
    return [cost, energy, emission]
}

function oil(x, y) {
    let cost = 0;
    let energy = 0;
    if(y == 'crude') {
        cost = 0.45*x;
        energy = 10500*x;
    } else if(y == 'gasoline') {
        cost = 1.1*x;
        energy = 9300*x;
    }
    let emission = 9300*x;
    return [cost, energy, emission]
}

function gas(x) {
    let cost = 0.12*x;
    let emission = 1.8*x;
    let energy = 10700*x;
    return [cost, energy, emission]
}