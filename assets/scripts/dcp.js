const compute = dcp.compute;

// broken event listener bc no go button
/* DONT USE WINDOW ONLOAD HERE THERE IS AN ONLOAD IN DOM.JS!!
window.onload = () => {
    document.getElementById('temp').onclick = () => {
        worker();
    }
}*/

let inputString = "we are going to lose sethacks woohoo"

function upperCaseFunction(letter) {
    progress();
    return letter.toUpperCase();
}

function workFunction(param) {
    progress();
    return "does something";
}

async function worker() {
    let inputSet = Array.from(inputString);
    let job = compute.for(inputSet, upperCaseFunction);
    job.public.name = "SETHACKS";

    job.computeGroups = [
        {
            joinKey: 'insight',
            joinSecret: 'dcp'
        }
    ]

    job.on('accepted', () => {
        console.log('Job Accepted, pending results...\nJob Id: ' + job.id);
    });
    job.on('result', (event) => {
        console.log('Result listener: ' + event.result);
    });
    job.on('complete', (result) => {
        console.log('Complete Result: ' + result);
    });

    let resultSet = await job.exec();
    resultSet = Array.from(resultSet);
  
    console.log(inputSet);
    console.log(resultSet);
    console.log("Job Complete");
}