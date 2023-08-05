depends = ('ITKPyBase', 'ITKStatistics', 'ITKSpatialObjects', 'ITKRegistrationMethodsv4', 'ITKMetricsv4', 'ITKImageStatistics', 'ITKImageSources', 'ITKImageIntensity', 'ITKImageGradient', 'ITKImageFunction', 'ITKImageCompose', 'ITKFFT', 'ITKDisplacementField', 'ITKCommon', 'ITKCommon', )
templates = (
  ('TimeVaryingVelocityFieldSemiLagrangianTransform', 'itk::TimeVaryingVelocityFieldSemiLagrangianTransform', 'itkTimeVaryingVelocityFieldSemiLagrangianTransformD2', True, 'double,2'),
  ('TimeVaryingVelocityFieldSemiLagrangianTransform', 'itk::TimeVaryingVelocityFieldSemiLagrangianTransform', 'itkTimeVaryingVelocityFieldSemiLagrangianTransformD3', True, 'double,3'),
  ('DataObjectDecorator', 'itk::DataObjectDecorator', 'itkDataObjectDecoratorTVVFSLTD2', False, 'itk::TimeVaryingVelocityFieldSemiLagrangianTransform< double, 2 >'),
  ('DataObjectDecorator', 'itk::DataObjectDecorator', 'itkDataObjectDecoratorTVVFSLTD3', False, 'itk::TimeVaryingVelocityFieldSemiLagrangianTransform< double, 3 >'),
  ('ImageRegistrationMethodv4', 'itk::ImageRegistrationMethodv4', 'itkImageRegistrationMethodv4IF2IF2TVVFSLTD2', False, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::TimeVaryingVelocityFieldSemiLagrangianTransform< double, 2 >'),
  ('ImageRegistrationMethodv4', 'itk::ImageRegistrationMethodv4', 'itkImageRegistrationMethodv4IF3IF3TVVFSLTD3', False, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::TimeVaryingVelocityFieldSemiLagrangianTransform< double, 3 >'),
  ('TimeVaryingVelocityFieldImageRegistrationMethodv4', 'itk::TimeVaryingVelocityFieldImageRegistrationMethodv4', 'itkTimeVaryingVelocityFieldImageRegistrationMethodv4IF2IF2TVVFSLT', False, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::TimeVaryingVelocityFieldSemiLagrangianTransform< double, 2 >'),
  ('TimeVaryingVelocityFieldImageRegistrationMethodv4', 'itk::TimeVaryingVelocityFieldImageRegistrationMethodv4', 'itkTimeVaryingVelocityFieldImageRegistrationMethodv4IF3IF3TVVFSLT', False, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::TimeVaryingVelocityFieldSemiLagrangianTransform< double, 3 >'),
  ('MetamorphosisImageRegistrationMethodv4', 'itk::MetamorphosisImageRegistrationMethodv4', 'itkMetamorphosisImageRegistrationMethodv4IF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('MetamorphosisImageRegistrationMethodv4', 'itk::MetamorphosisImageRegistrationMethodv4', 'itkMetamorphosisImageRegistrationMethodv4IF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('WrapExtrapolateImageFunction', 'itk::WrapExtrapolateImageFunction', 'itkWrapExtrapolateImageFunctionISS2D', True, 'itk::Image< signed short,2 >,double'),
  ('WrapExtrapolateImageFunction', 'itk::WrapExtrapolateImageFunction', 'itkWrapExtrapolateImageFunctionIUC2D', True, 'itk::Image< unsigned char,2 >,double'),
  ('WrapExtrapolateImageFunction', 'itk::WrapExtrapolateImageFunction', 'itkWrapExtrapolateImageFunctionIUS2D', True, 'itk::Image< unsigned short,2 >,double'),
  ('WrapExtrapolateImageFunction', 'itk::WrapExtrapolateImageFunction', 'itkWrapExtrapolateImageFunctionIF2D', True, 'itk::Image< float,2 >,double'),
  ('WrapExtrapolateImageFunction', 'itk::WrapExtrapolateImageFunction', 'itkWrapExtrapolateImageFunctionISS3D', True, 'itk::Image< signed short,3 >,double'),
  ('WrapExtrapolateImageFunction', 'itk::WrapExtrapolateImageFunction', 'itkWrapExtrapolateImageFunctionIUC3D', True, 'itk::Image< unsigned char,3 >,double'),
  ('WrapExtrapolateImageFunction', 'itk::WrapExtrapolateImageFunction', 'itkWrapExtrapolateImageFunctionIUS3D', True, 'itk::Image< unsigned short,3 >,double'),
  ('WrapExtrapolateImageFunction', 'itk::WrapExtrapolateImageFunction', 'itkWrapExtrapolateImageFunctionIF3D', True, 'itk::Image< float,3 >,double'),
)
snake_case_functions = ('metamorphosis_image_registration_methodv4', 'time_varying_velocity_field_image_registration_methodv4', 'image_registration_methodv4', )
