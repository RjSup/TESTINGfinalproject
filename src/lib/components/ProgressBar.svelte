<script>
    export let currentStep;
    export let totalSteps;
</script>

<div class="mb-8">
    <div class="h-1 bg-gray-100 rounded-full">
        <div 
            class="h-1 bg-green-500 rounded-full transition-all duration-300" 
            style="width: {((currentStep + 1) / totalSteps) * 100}%"
        >
        </div>
    </div>
    <p class="mt-2 text-sm text-gray-500 text-right">Step {currentStep + 1} of {totalSteps}</p>
</div>