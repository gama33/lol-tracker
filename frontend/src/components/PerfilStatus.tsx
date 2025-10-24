import './PerfilStatus.css'

function PerfilStatus() {
  return (
    <div className='bg-gray-800 rounded-xl shadow-lg p-6'>
        <div className='flex'>
            {/* bloco de perfil */}
            <div> 
                <div className='flex items-center gap-4'>
                    {/* icone */}
                    <div>
                        <p>icone</p>
                    </div>

                    {/* info */}
                    <div>
                        <p>info</p>
                    </div>
                </div>
            </div>

            {/* bloco de estatistica */}
            <div>

            </div>
        </div>
    </div>
  )
}

export default PerfilStatus