################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Drivers/nRF24/Src/MY_NRF24.c 

OBJS += \
./Drivers/nRF24/Src/MY_NRF24.o 

C_DEPS += \
./Drivers/nRF24/Src/MY_NRF24.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/nRF24/Src/MY_NRF24.o: ../Drivers/nRF24/Src/MY_NRF24.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU GCC Compiler'
	@echo $(PWD)
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -mfloat-abi=soft -DUSE_HAL_DRIVER -DSTM32F042x6 -I"/home/bugi/STM32/Projects/STM32nRF24TX/Inc" -I"/home/bugi/STM32/Projects/STM32nRF24TX/Drivers/nRF24/Inc" -I"/home/bugi/STM32/Projects/STM32nRF24TX/Drivers/STM32F0xx_HAL_Driver/Inc" -I"/home/bugi/STM32/Projects/STM32nRF24TX/Drivers/STM32F0xx_HAL_Driver/Inc/Legacy" -I"/home/bugi/STM32/Projects/STM32nRF24TX/Drivers/CMSIS/Device/ST/STM32F0xx/Include" -I"/home/bugi/STM32/Projects/STM32nRF24TX/Drivers/CMSIS/Include"  -Og -g3 -Wall -fmessage-length=0 -ffunction-sections -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


