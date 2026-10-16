import { expect, test } from '@playwright/test';

test('high-risk capacity requirement produces reviewable test ideas', async ({ page }) => {
  await page.goto('/#quality-lab');
  await page.getByRole('button', { name: 'Suggest test scenarios' }).click();

  await expect(page.getByText('Provider: rules')).toBeVisible();
  await expect(page.getByText('Final available place is allocated exactly once')).toBeVisible();
  await expect(page.getByText('Cancellation promotes the oldest wait-listed user')).toBeVisible();
  await expect(page.getByText(/human review/i)).toBeVisible();
});

test('page keeps a stable visual baseline at desktop width', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium', 'Desktop Chromium owns the canonical baseline.');
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto('/');
  await expect(page).toHaveScreenshot('civicshift-home.png', {
    fullPage: true,
    animations: 'disabled',
    maxDiffPixelRatio: 0.02,
    mask: [page.locator('.status-pill')],
  });
});
