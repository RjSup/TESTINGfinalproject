<script>
    export let summary;
</script>

<div class="border-t pt-6">
    <h2 class="text-xl font-medium text-gray-900 mb-4">Investment Summary</h2>
    <div class="bg-gray-50 p-4 rounded-lg space-y-3">
        <div class="flex justify-between items-center">
            <span class="text-gray-600">Initial Investment</span>
            <span class="font-medium">£{summary.initial_investment.toLocaleString()}</span>
        </div>
        <div class="flex justify-between items-center">
            <span class="text-gray-600">Predicted Future Value</span>
            <span class="font-medium text-green-600">£{summary.predicted_portfolio_value.toLocaleString()}</span>
        </div>
        <div class="flex justify-between items-center">
            <span class="text-gray-600">Potential Gain</span>
            <span class="font-medium text-green-600">£{summary.total_predicted_gain.toLocaleString()}</span>
        </div>
        <div class="flex justify-between items-center">
            <span class="text-gray-600">Total Return</span>
            <span class="font-medium text-green-600">{summary.total_return_percentage}%</span>
        </div>
    </div>
</div>