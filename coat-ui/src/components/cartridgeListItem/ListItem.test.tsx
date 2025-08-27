import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { vi } from 'vitest';
import ListItem from './ListItem';

describe("ListItem tests", () => {
    const def_props = {
        id: 1,
        type: 'SampleType',
        status: 'P',
        color: 'red',
        isChecked: vi.fn(() => false),
    };


    test("topContent and bottomContent rendering", () => {
        render(<ListItem
            {...def_props}
            topContent='top'
            bottomContent='bottom'
        />)
        
        expect(screen.getByText('top')).toBeInTheDocument();
        expect(screen.getByText('bottom')).toBeInTheDocument();
    })

    test("N/A fallback rendering", () => {
        render(<ListItem {...def_props} />);
        const naTexts = screen.getAllByText('N/A');
        expect(naTexts.length).toBeGreaterThanOrEqual(2);
    });

    it('renders "?" when status is neither P nor F and showMark = true', () => {
        render(<ListItem {...def_props} status="UNKNOWN" showMark />);
        expect(screen.getByText('?')).toBeInTheDocument();
    });

    it('does not render a status icon when showMark = false', () => {
        render(<ListItem {...def_props} showMark={false} />);
        expect(screen.queryByText('?')).not.toBeInTheDocument();
    });

    it('renders the type label with a colored dot', () => {
        render(<ListItem {...def_props} type="CustomType" color="blue" />);
        expect(screen.getByText('CustomType')).toBeInTheDocument();

        const dot = screen.getByTestId('colored-dot');
        expect(getComputedStyle(dot).backgroundColor).toBe('rgb(0, 0, 255)');
    });
})


