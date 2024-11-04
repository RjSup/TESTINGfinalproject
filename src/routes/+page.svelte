<script>
    import ProgressBar from '$lib/components/ProgressBar.svelte';
    import QuestionForm from '$lib/components/QuestionForm.svelte';
    import InvestmentSummary from '$lib/components/InvestmentSummary.svelte';
    import PortfolioDetails from '$lib/components/PortfolioDetails.svelte';
    import NavBar from '$lib/components/NavBar.svelte';

    let investmentAmount = '';
    let currentSavings = '';
    let riskTolerance = 5;
    let industryPreference = '';
    let loading = false;
    let error = null;
    let result = null;
    let questionIndex = 0;

    const questions = [
        { label: 'Investment Amount', bindVar: 'investmentAmount', placeholder: 'Enter amount', type: 'number' },
        { label: 'Current Savings', bindVar: 'currentSavings', placeholder: 'Enter savings', type: 'number' },
        { label: 'Risk Tolerance', bindVar: 'riskTolerance', type: 'range', min: 1, max: 10 },
        { label: 'Preferred Industry', bindVar: 'industryPreference', placeholder: 'e.g., Technology, Healthcare', type: 'text' }
    ];

    async function handleNext() {
        if (questionIndex < questions.length - 1) {
            questionIndex += 1;
        } else {
            await handleSubmit();
        }
    }

    async function handleSubmit() {
        loading = true;
        error = null;
        result = null;

        try {
            const payload = {
                investment_amount: Number(investmentAmount),
                current_savings: Number(currentSavings),
                risk_tolerance: Number(riskTolerance),
                industry: industryPreference
            };

            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (!data.success) throw new Error(data.error || 'Calculation failed');
            result = data;
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    }
</script>

<NavBar />

<div class="min-h-screen w-full bg-white px-4 py-12">
    <div class="max-w-xl mx-auto">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">WealthWise</h1>
        
        <ProgressBar 
            currentStep={questionIndex} 
            totalSteps={questions.length} 
        />

        {#if questionIndex < questions.length}
            <QuestionForm
                question={questions[questionIndex]}
                bind:investmentAmount
                bind:currentSavings
                bind:riskTolerance
                bind:industryPreference
                onNext={handleNext}
                isLastQuestion={questionIndex === questions.length - 1}
            />
        {/if}

        {#if error}
            <div class="mt-6 p-4 text-red-600 bg-red-50 rounded-lg">
                <p>{error}</p>
            </div>
        {/if}

        {#if result}
            <InvestmentSummary summary={result.summary} />
            <PortfolioDetails 
                portfolio={result.portfolio}
                rebalanceDate={result.summary.rebalance_date}
            />
        {/if}
    </div>
</div>