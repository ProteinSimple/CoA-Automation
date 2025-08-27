import { render, screen, fireEvent  } from "@testing-library/react";
import '@testing-library/jest-dom';
import CloseButton from "./CloseButton";
import { vi } from 'vitest';



describe('CloseButton', () => {
  it('renders the button with "X"', () => {
    render(<CloseButton onClick={() => {}} />);
    expect(screen.getByRole('button', { name: /x/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<CloseButton onClick={handleClick} />);
    const button = screen.getByRole('button', { name: /x/i });

    fireEvent.click(button);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});