import { useQuery } from '@tanstack/react-query'
import api from '../../lib/api'

export default function GuestInfo() {
  const { data: content, isLoading } = useQuery({
    queryKey: ['content'],
    queryFn: async () => {
      const response = await api.get('/content')
      return response.data
    },
  })

  if (isLoading) {
    return <div className="text-center py-12">Loading...</div>
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">
        Wedding Information
      </h1>
      
      {content && content.length > 0 ? (
        <div className="space-y-6">
          {content.map((item) => (
            <div key={item.id} className="bg-white rounded-lg shadow-lg p-8">
              {item.title && (
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                  {item.title}
                </h2>
              )}
              <div
                className="text-gray-700 prose max-w-none"
                dangerouslySetInnerHTML={{ __html: item.content }}
              />
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <p className="text-gray-600">Wedding information will be posted here soon.</p>
        </div>
      )}
    </div>
  )
}

