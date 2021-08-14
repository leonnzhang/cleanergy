const compute = dcp.compute;

// broken event listener bc no go button
window.onload = () => {
    document.getElementById('go').onclick = () => {
        worker();
    }
}

function upperCaseFunction(letter) {
    progress();
    return letter.toUpperCase();
}

function workFunction() {
    progress();
    return "does something";
}

async function worker() {
    let inputSet = Array.from(inputString);
    let job = compute.for(inputSet, workFunction);

    job.computeGroups = [
        {
            joinKey: 'sethacks',
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