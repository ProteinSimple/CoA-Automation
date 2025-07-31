interface CloseButtonProps {
  onClick: () => void;
}

function CloseButton({ onClick } : CloseButtonProps) {

  return (
    <button className='setting_x' onClick={onClick}> X </button>
  )
}


export default CloseButton;
