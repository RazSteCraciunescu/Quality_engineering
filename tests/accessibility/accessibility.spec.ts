import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test('landing and event list have no serious automated accessibility violations', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Choose a volunteer shift' })).toBeVisible();
  const result = await new AxeBuilder({ page }).analyze();
  const serious = result.violations.filter((item) => ['serious', 'critical'].includes(item.impact ?? ''));
  expect(serious).toEqual([]);
});

test('booking dialog has a name, labels and keyboard focus target', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Reserve a place' }).first().click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await expect(page.getByLabel('Full name')).toBeFocused();
  const result = await new AxeBuilder({ page }).include('.modal-card').analyze();
  expect(result.violations.filter((item) => item.impact === 'critical')).toEqual([]);
});
