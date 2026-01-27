import { test, expect } from '@playwright/test';

test.describe('CascadeGuard SCF - Production E2E Suite', () => {

    test.beforeEach(async ({ page }) => {
        await page.goto('http://localhost:5173/');
        await page.waitForTimeout(3000); // Allow React hydration + lazy loading
    });

    // =========================================================================
    // HAPPY PATH TESTS
    // =========================================================================

    test('Happy Path: Dashboard Branding and Title', async ({ page }) => {
        await expect(page.locator('h1')).toContainText('CASCADEGUARD');
        await expect(page.getByText('AUDIT V9.0')).toBeVisible();
    });

    test('Happy Path: Global Metrics Are Displayed', async ({ page }) => {
        // Wait for data load confirmation
        await expect(page.getByText('LIVE ENGINE DATA')).toBeVisible();

        await expect(page.getByText('GLOBAL METRICS')).toBeVisible();
        await expect(page.getByText('Spectral Radius (λ₁)')).toBeVisible();
        await expect(page.getByText('25.00')).toBeVisible(); // Live Spectral Radius
        await expect(page.getByText('€90.0M')).toBeVisible(); // Live Expected Loss
    });

    test('Happy Path: Schematic View Is Active', async ({ page }) => {
        await expect(page.getByText('LIVE ENGINE DATA')).toBeVisible();
        // Check if the schematic image is loaded
        const image = page.locator('img[alt="Supply Chain Schematic"]');
        await expect(image).toBeVisible();
    });

    test('Happy Path: Audit Button is Present and Clickable', async ({ page }) => {
        const auditBtn = page.getByRole('button', { name: /REFRESH AUDIT/i });
        await expect(auditBtn).toBeVisible();
        await auditBtn.click();
        // Button should remain functional (no crash)
    });

    // =========================================================================
    // ALERT TESTS
    // =========================================================================

    test('Alert: Critical TSMC Alert Is Visible', async ({ page }) => {
        await expect(page.getByText('CRITICAL ALERTS')).toBeVisible();

        const tsmcAlert = page.locator('.col-span-3').filter({ hasText: 'TSMC' });
        await expect(tsmcAlert).toBeVisible();
        await expect(tsmcAlert).toContainText('CRITICAL');
        await expect(tsmcAlert).toContainText('Single Point of Failure');
    });

    // =========================================================================
    // EDGE CASE TESTS
    // =========================================================================

    test('Edge Case: Responsive Layout on Mobile Viewport', async ({ page }) => {
        await page.setViewportSize({ width: 375, height: 812 }); // iPhone X
        await page.waitForTimeout(500);

        // Core elements should still be visible
        await expect(page.locator('h1')).toBeVisible();
        // Use a more generic check or specific mobile element if available.
        // For now, ensuring the H1 is there implies the app didn't crash.
    });

    test('Edge Case: Large Viewport (4K Monitor)', async ({ page }) => {
        await page.setViewportSize({ width: 3840, height: 2160 });
        await page.waitForTimeout(500);

        await expect(page.locator('h1')).toBeVisible();
        await expect(page.getByText('TSMC')).toBeVisible();
    });

    // =========================================================================
    // API INTEGRATION TESTS
    // =========================================================================

    test('API: Backend Health Check', async ({ page }) => {
        const response = await page.request.get('http://localhost:11885/health');
        expect(response.ok()).toBeTruthy();
        const data = await response.json();
        expect(data.status).toBe('CascadeGuard Engine Online');
        expect(data.version).toBe('9.0-Industrial');
    });

});
