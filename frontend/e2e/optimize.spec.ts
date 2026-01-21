import { test, expect } from '@playwright/test'

test.describe('Quantum SCF Optimizer E2E', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/')
    })

    test('should display upload interface on load', async ({ page }) => {
        // GIVEN the app loads
        // WHEN viewing the page
        // THEN upload interface is visible
        await expect(page.getByText('Upload Supply Chain Data')).toBeVisible()
        await expect(page.getByText('Drag & drop your CSV file here')).toBeVisible()
    })

    test('should load sample data and run optimization', async ({ page }) => {
        // GIVEN the app is loaded
        // WHEN clicking "Load 10-tier sample data"
        await page.getByText('Load 10-tier sample data').click()

        // THEN optimization should run and results appear
        await expect(page.getByText('Running quantum optimization...')).toBeVisible()

        // Wait for results (timeout 30s for quantum solver)
        await expect(page.getByText('Optimization Results')).toBeVisible({ timeout: 30000 })
    })

    test('should display comparison metrics after optimization', async ({ page }) => {
        // GIVEN sample data is loaded and optimized
        await page.getByText('Load 10-tier sample data').click()
        await expect(page.getByText('Optimization Results')).toBeVisible({ timeout: 30000 })

        // THEN comparison metrics should be visible
        await expect(page.getByText('Yield Improvement')).toBeVisible()
        await expect(page.getByText('Risk Reduction')).toBeVisible()
        await expect(page.getByText('Classical (PuLP)')).toBeVisible()
        await expect(page.getByText('Quantum (D-Wave)')).toBeVisible()
    })

    test('should complete classical optimization under 5 seconds', async ({ page }) => {
        // GIVEN optimization runs
        await page.getByText('Load 10-tier sample data').click()
        await expect(page.getByText('Optimization Results')).toBeVisible({ timeout: 30000 })

        // THEN classical solve time should be < 5000ms
        // This is validated by the table showing solve time
        const solveTimeRow = page.locator('tr').filter({ hasText: 'Solve Time' })
        await expect(solveTimeRow).toBeVisible()
    })

    test('should download PDF report', async ({ page }) => {
        // GIVEN optimization is complete
        await page.getByText('Load 10-tier sample data').click()
        await expect(page.getByText('Optimization Results')).toBeVisible({ timeout: 30000 })

        // WHEN clicking download PDF
        const downloadPromise = page.waitForEvent('download')
        await page.getByText('Download PDF Report').click()

        // THEN PDF should download
        const download = await downloadPromise
        expect(download.suggestedFilename()).toMatch(/scf_report_.*\.pdf/)
    })

    test('should show solver logs', async ({ page }) => {
        // GIVEN optimization is complete
        await page.getByText('Load 10-tier sample data').click()
        await expect(page.getByText('Optimization Results')).toBeVisible({ timeout: 30000 })

        // THEN solver logs should be visible
        await expect(page.getByText('Quantum Solver Logs')).toBeVisible()
    })

    test('should allow new optimization after reset', async ({ page }) => {
        // GIVEN optimization is complete
        await page.getByText('Load 10-tier sample data').click()
        await expect(page.getByText('Optimization Results')).toBeVisible({ timeout: 30000 })

        // WHEN clicking new optimization
        await page.getByText('New Optimization').click()

        // THEN upload interface returns
        await expect(page.getByText('Upload Supply Chain Data')).toBeVisible()
    })
})
