import { expect, test } from '@playwright/test';

test.describe('volunteer registration', () => {
  test('eligible visitor reserves a place and receives a reference', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Choose a volunteer shift' })).toBeVisible();

    await page.getByRole('button', { name: 'Reserve a place' }).first().click();
    await page.getByLabel('Full name').fill('Playwright Volunteer');
    await page.getByLabel('Email address').fill(`playwright-${Date.now()}@example.test`);
    await page.getByLabel('Age').fill('29');
    await page.getByLabel(/privacy notice/i).check();
    await page.getByRole('button', { name: 'Confirm registration' }).click();

    await expect(page.getByRole('heading', { name: 'Your place is confirmed.' })).toBeVisible();
    await expect(page.getByText(/Reference: reg-/)).toBeVisible();
  });

  test('age boundary is explained without losing the form state', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: 'Reserve a place' }).nth(1).click();
    await page.getByLabel('Full name').fill('Young Volunteer');
    await page.getByLabel('Email address').fill(`young-${Date.now()}@example.test`);
    await page.getByLabel('Age').fill('17');
    await page.getByLabel(/privacy notice/i).check();
    await page.getByRole('button', { name: 'Confirm registration' }).click();

    await expect(page.getByRole('alert')).toContainText('at least 18');
    await expect(page.getByLabel('Full name')).toHaveValue('Young Volunteer');
  });

  test('escape closes the registration dialog', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: 'Reserve a place' }).first().click();
    await expect(page.getByRole('dialog')).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.getByRole('dialog')).toBeHidden();
  });
});
