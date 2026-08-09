export const Notification = ({ message }) => {
    console.log('Notification message:', message) 
  if (message === null) {
    return null
  }

  return (
    <div className="notification">
      {message}
    </div>
  )
}
export const ErrorNotification = ({ message }) => {
    console.log('ErrorNotification message:', message) 
    if (message === null) {
        return null
    }   
    return (
        <div className="errorNotification">
            {message}
        </div>
    )
}

