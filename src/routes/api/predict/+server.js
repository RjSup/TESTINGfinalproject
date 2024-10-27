import { json } from '@sveltejs/kit';
import { spawn } from 'child_process';

export async function POST({ request }) {
    console.log('API endpoint hit');

    try {
        // Get the data from the request
        const data = await request.json();
        console.log('Received data:', data);

        // Run the Python process and store its output
        return new Promise((resolve) => {
            const pythonProcess = spawn('python3', ['src/lib/ML/ml.py']);
            let outputData = '';

            // Collect the output from Python
            pythonProcess.stdout.on('data', (data) => {
                outputData += data.toString();
                console.log('Python output:', data.toString());
            });

            // Collect errors from Python output
            pythonProcess.stderr.on('data', (data) => {
                console.error('Python stderr:', data.toString());
            });

            // After Python code is done running
            pythonProcess.on('close', (code) => {
                console.log('Python process closed with code:', code);
                
                // Parse the Python output as JSON
                try {
                    const result = JSON.parse(outputData.trim());
                    resolve(json(result));
                } catch (error) {
                    console.error('Parse error:', error);
                    resolve(json({ success: false, error: 'Failed to parse Python output' }));
                }
            });

            // Send user input to Python script
            pythonProcess.stdin.write(JSON.stringify(data));
            pythonProcess.stdin.end();
        });
    } catch (error) {
        console.error('Server error:', error);
        return json({ success: false, error: error.message });
    }
}
