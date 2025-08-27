import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { vi } from 'vitest';
import Checkbox from './Checkbox';


describe('Checkbox tests', () => {
    test('unchecked rendering correct', () => {
        const isChecked = vi.fn(() => false)
        render(<Checkbox id="testbox" isChecked={isChecked}/>)
        const input = screen.getByRole('checkbox')
        expect(input).not.toBeChecked();
    })

    test('checked rendering correct', () => {
        const isChecked = vi.fn(() => false)
        render(<Checkbox id="testbox" isChecked={isChecked}/>)
        const input = screen.getByRole('checkbox')
        expect(input).not.toBeChecked();
    })

    test('state change testing', () => {
        

        let checked = false;
        const isChecked = vi.fn(() => checked)

        const onChecked = vi.fn(() => {
            checked = true
        });
        const onUnchecked = vi.fn(() => {
            checked = false
        });
        render(<Checkbox
            id='testbox'
            onChecked={onChecked}
            onUnchecked={onUnchecked}
            isChecked={isChecked}
            
        />)

        const input = screen.getByRole('checkbox')
        fireEvent.click(input);
        expect(onChecked).toHaveBeenCalledTimes(1)
        expect(onUnchecked).not.toHaveBeenCalled();
        expect(checked).toEqual(true);

        fireEvent.click(input);
        expect(onChecked).toHaveBeenCalledTimes(1)
        expect(onUnchecked).toHaveBeenCalledTimes(1);
        expect(checked).toEqual(false);
    })

})